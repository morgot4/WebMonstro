from .schemas import ProfileRead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql  import func, not_
from fastapi import Depends, Path
from core.models import db_helper
from .crud import *
from typing import Annotated
from time import sleep
from core.config import settings
import logging

logger = logging.getLogger("my_app")



async def profile_by_pid(pid: Annotated[int, Path] , session: AsyncSession = Depends(db_helper.session_dependency)) -> ProfileRead:
    return await get_profile_by_pid(pid=pid, session=session)

async def profiles_by_party(party: Annotated[str, Path], session: AsyncSession = Depends(db_helper.session_dependency)) -> list[ProfileRead]:
    return await get_profiles_by_party(party=party, session=session)

async def check_working_party_for_append():
    async with db_helper.session_factory() as session:

        #get count of profiles
        query = select(func.count()).select_from(ProfilesOrm).where(ProfilesOrm.party == settings.profiles.WORKING_PARTY)
        res = await session.execute(query)
        profiles_count = res.scalar()
        logger.info(f"Get {settings.profiles.WORKING_PARTY} capacity for append to {settings.profiles.WORKING_PARTY}: {profiles_count}")
        #if not enought profiles, append new
        if profiles_count < settings.profiles.NORMAL_WORKING_PARTY_CAPACITY:
            #not enought count
            shortage = settings.profiles.NORMAL_WORKING_PARTY_CAPACITY - profiles_count
            #min and max correct date
            min_date, max_date = hours_to_dates(settings.profiles.MIN_LIFE_HOURS_TO_WORKING_PARTY, settings.profiles.MAX_LIFE_HOURS_TO_WORKING_PARTY)
            logger.info(f"Search profile before {min_date} ")
            query = select(ProfilesOrm.party, func.count()).select_from(ProfilesOrm).where(and_(
                        ProfilesOrm.party.like("s_%"),
                        ProfilesOrm.data_create.between(min_date, max_date),
                        ProfilesOrm.date_block < (func.now() - text(f"interval '{settings.profiles.TIME_BEFORE_DATE_BLOCK} hours'")),

                    )).filter(not_(ProfilesOrm.folder.op('~')('^(1,)*1$'))).group_by(ProfilesOrm.party)
            res = await session.execute(query)
            parties= res.scalars().all()
    
            logger.info(f"get s_ parties, count: {len(parties)}")
            if len(parties) != 0:
                party_fraction = shortage // len(parties)
                if party_fraction != 0:
                    await servers_parties_to_s_mix(session=session, party_fraction=party_fraction, parties=parties, min_date=min_date, max_date=max_date)


async def from_working_parties_to_trash_party(trash_party: str = settings.profiles.TRASH_PARTY, big_age_party = "s_>72"):
    async with db_helper.session_factory() as session:
        max_date = hours_to_dates(max_hours_life=settings.profiles.MAX_LIFE_HOURS_TO_WORKING_PARTY)
        query = select(ProfilesOrm.pid, ProfilesOrm.folder, ProfilesOrm.data_create).where(and_(ProfilesOrm.party == "s_mix", ProfilesOrm.data_create > max_date))
        res = await session.execute(query)
        profiles = res.all()
        logger.info(f"Get capacity of s_ for cleaning to A: {len(profiles)}")
        for profile in profiles:
            print(profile)
            if len(list(set(profile[1].split(",")))) > 1:
                update_stmt = (
                update(ProfilesOrm)
                .where(ProfilesOrm.pid == profile[0])
                .values(
                    party=trash_party,
                    last_date_work=ProfilesOrm.last_date_work,
                    date_block=ProfilesOrm.date_block,
                    warm=ProfilesOrm.warm
                )
            )
                logger.info(f"Set profile {profile[0]} with folder {profile[1]} to {trash_party} party")
                await session.execute(update_stmt)
                await session.commit()

        query = select(ProfilesOrm.pid, ProfilesOrm.folder).where(and_(ProfilesOrm.party.like("s_%"), ProfilesOrm.data_create <= max_date))
        res = await session.execute(query)
        profiles = res.all()
        logger.info(f"Get s_ capacity for cleaning to s_>72: {len(profiles)}")
        for profile in profiles:
            update_stmt = (
                update(ProfilesOrm)
                .where(ProfilesOrm.pid == profile[0])
                .values(
                    party=big_age_party,
                    last_date_work=ProfilesOrm.last_date_work,
                    date_block=ProfilesOrm.date_block,
                    warm=ProfilesOrm.warm
                )
            )
            # logger.info(f"Set profile {profile[0]} with folder {profile[1]} to {big_age_party} party")
            await session.execute(update_stmt)
            await session.commit()
