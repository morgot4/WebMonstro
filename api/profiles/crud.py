from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.types import TIMESTAMP
from sqlalchemy import select, delete
from sqlalchemy import and_
from fastapi import Depends
from core.models.profiles import ProfilesOrm
from core.models import db_helper
import datetime
from api.utils.date_tools import add_remove_hours_with_tz, hours_to_datetime_with_tz

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

async def setup_profiles_by_parameters(session: AsyncSession, parties: list[str], new_party, profiles_count, min_len_folder, max_len_folder, min_age, max_age):
    party_fraction = profiles_count // len(parties)
    for party in parties:
        now = datetime.datetime.now(datetime.timezone.utc)
        min_date = add_remove_hours_with_tz(now, min_age, remove=True)
        max_date = add_remove_hours_with_tz(now, max_age, remove=True)
        print(min_date, max_date)
        query = select(ProfilesOrm).where(ProfilesOrm.party == party).where(ProfilesOrm.warm.between(min_date, max_date)).limit(party_fraction)
        res = await session.execute(query)
        for profile in res.scalars().all():
            print(print(profile.folder, profile.warm))
        
