import asyncio
import random

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import *
from src.infrastructure.database import sessionmanager

async def insert_test_data():
    async with sessionmanager.session() as session:
        session: AsyncSession

        users = [
            UserTable(id=1, username='admin', password_hash='hashed_password_1'),
            UserTable(id=2, username='user1', password_hash='hashed_password_2'),
            UserTable(id=3, username='user2', password_hash='hashed_password_3'),
        ]
        session.add_all(users)

        api_keys = [
            APIKeyTable(id=1, user_id=1, key='apikey_123456'),
            APIKeyTable(id=2, user_id=2, key='apikey_abcdef'),
            APIKeyTable(id=3, user_id=3, key='apikey_789xyz'),
        ]
        session.add_all(api_keys)

        buildings = [
            BuildingTable(id=i, address=f'Building {i}', latitude=round(random.uniform(-90, 90.0), 1), longitude=round(random.uniform(-180.0, 180.0), 1))
            for i in range(1, 11)
        ]
        session.add_all(buildings)

        organizations = [
            OrganizationTable(id=i, name=f'Organization {i}', building_id=i)
            for i in range(1, 11)
        ]
        session.add_all(organizations)

        phone_numbers = [
            PhoneNumberTable(id=i, organization_id=i, phone_number=f'+12345678{i}')
            for i in range(1, 11)
        ]
        session.add_all(phone_numbers)

        activities = [
            ActivityTable(id=1, name='Technology', parent_id=None),
            ActivityTable(id=2, name='Healthcare', parent_id=None),
            ActivityTable(id=3, name='Education', parent_id=None),
            ActivityTable(id=4, name='Software Development', parent_id=1),
            ActivityTable(id=5, name='Medical Services', parent_id=2),
            ActivityTable(id=6, name='Finance', parent_id=None),
            ActivityTable(id=7, name='Retail', parent_id=None),
            ActivityTable(id=8, name='Consulting', parent_id=None),
            ActivityTable(id=9, name='Manufacturing', parent_id=None),
            ActivityTable(id=10, name='Media', parent_id=None),
            ActivityTable(id=11, name='Logistics', parent_id=None),
            ActivityTable(id=12, name='Energy', parent_id=None),
            ActivityTable(id=13, name='AI Research', parent_id=4),
            ActivityTable(id=14, name='E-commerce', parent_id=7),
            ActivityTable(id=15, name='Cybersecurity', parent_id=4),
            ActivityTable(id=16, name='Pharmaceuticals', parent_id=5),
            ActivityTable(id=17, name='Marketing', parent_id=10),
            ActivityTable(id=18, name='Data Science', parent_id=13),
            ActivityTable(id=19, name='Legal Services', parent_id=8),
            ActivityTable(id=20, name='Sustainable Energy', parent_id=12),
        ]
        session.add_all(activities)
        await session.commit()

        organization_activity_data = [
            (1, 1), (2, 3), (2, 4), (3, 5), (3, 6), (3, 20),
            (4, 17), (4, 18), (6, 7), (6, 8), (6, 9), (7, 19),
            (8, 13), (8, 14), (8, 11), (9, 15), (9, 16), (9, 6)
        ]
        for org_id, act_id in organization_activity_data:
            stmt = organization_activity.insert().values(organization_id=org_id, activity_id=act_id)
            await session.execute(stmt)

        user_organization_data = [
            (1, 1), (2, 2), (3, 3), (1, 4), (2, 5), (3, 6),
            (1, 7), (2, 8), (3, 9), (1, 10)
        ]
        for user_id, org_id in user_organization_data:
            stmt = user_organization.insert().values(user_id=user_id, organization_id=org_id)
            await session.execute(stmt)

        await session.commit()

if __name__ == '__main__':
    asyncio.run(insert_test_data())
