from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.types import TIMESTAMP
from sqlalchemy import select, delete, update
from sqlalchemy.sql import func, and_, text, not_
from fastapi import Depends
from core.models import ProfilesOrm
from core.models import db_helper
import datetime
import logging
from core.config import settings


logger = logging.getLogger('my_app')

def hours_to_dates(min_hours_life = 0, max_hours_life = 0):
    """get dates interval (min and max dates) from min and max hours of life"""

    min_days = min_hours_life // 24
    min_hours = min_hours_life % 24
    max_days = max_hours_life // 24
    max_hours = max_hours_life % 24
    max_interval = text(f"interval '{min_days} days {min_hours} hours'")
    min_interval = text(f"interval '{max_days} days {max_hours} hours'")
    if min_hours_life == 0:
        return func.now() - min_interval
    elif max_hours_life == 0:
        return func.now() - max_interval
    return func.now() - min_interval, func.now() - max_interval


async def get_profile_by_pid(pid: int, session: AsyncSession):
    return await session.get(ProfilesOrm, pid)
    
async def get_profiles_by_party(party: str, session: AsyncSession):
    query = select(ProfilesOrm).where(ProfilesOrm.party == party)
    res = await session.execute(query)
    print(res)
    return res.scalars().all()

async def delete_profiles_by_time(time: datetime.datetime, session: AsyncSession):
    query = delete(ProfilesOrm).where(ProfilesOrm.data_create <= datetime.datetime.now(datetime.timezone.utc) - time)
    res = await session.execute(query)
    print(res)


async def update_profile(profile: ProfilesOrm, session: AsyncSession, profile_update: ProfilesOrm):
    for name, value in profile_update.model_dump(exclude_unset=True).items():
        setattr(profile, name, value)
    await session.commit()
    return profile


async def servers_parties_to_s_mix(session: AsyncSession, party_fraction, parties, min_date, max_date, new_party: str = "s_mix"):

    for party in parties:
        selected_ids = (
                select(ProfilesOrm)
                .where(
                    and_(
                        ProfilesOrm.party == party,
                        ProfilesOrm.data_create.between(min_date, max_date),
                        ProfilesOrm.date_block < (func.now() - text(f"interval '{settings.profiles.TIME_BEFORE_DATE_BLOCK} hours'")),
                        ProfilesOrm.folder.op("~")("^([1,]+)$"),
                        not_(ProfilesOrm.folder.op("~")("[^1,]"))
                    )
                )
                .limit(party_fraction)
                .cte("selected_ids")
            )

        update_stmt = (
            update(ProfilesOrm)
            .where(ProfilesOrm.pid.in_(select(selected_ids.c.pid)))
            .values(
                party=new_party,
                last_date_work=ProfilesOrm.last_date_work,
                date_block=func.now(),
                warm=ProfilesOrm.warm
            )
        )

        await session.execute(update_stmt)
        logger.info(f"For party {party} update {party_fraction} profiles to new party: {new_party}")
        await session.commit()
        

async def setup_profiles_by_parameters(session: AsyncSession, parties: list[str], new_party, profiles_count, min_hours_life, max_hours_life):
    party_fraction = profiles_count // len(parties)
    max_date, min_date = hours_to_dates(min_hours_life, max_hours_life)
    
    for party in parties:
        selected_ids = (
            select(ProfilesOrm.pid)
            .where(
                and_(
                    ProfilesOrm.party == party,
                    ProfilesOrm.data_create.between(
                        min_date,
                        max_date
                    )
                )
            )
            .limit(party_fraction)
            .cte("selected_ids")
        )

        update_stmt = (
            update(ProfilesOrm)
            .where(ProfilesOrm.pid.in_(select(selected_ids.c.pid)))
            .values(
                party=new_party,
                last_date_work=ProfilesOrm.last_date_work,
                date_block=ProfilesOrm.date_block,
                warm=ProfilesOrm.warm
            )
        )

        res = await session.execute(update_stmt)
        print(res.scalars().all())
        await session.commit()
    
    return party_fraction * len(parties)
        
