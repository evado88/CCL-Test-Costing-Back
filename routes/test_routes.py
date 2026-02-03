from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from models.test_model import Test, TestDB, TestWithDetail
from models.user_model import UserDB

router = APIRouter(prefix="/tests", tags=["Tests"])


@router.post("/create", response_model=TestWithDetail)
async def create(test: Test, db: AsyncSession = Depends(get_db)):
    # check user exists
    result = await db.execute(select(UserDB).where(UserDB.id == test.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=400, detail=f"The user with id '{test.user_id}' does not exist"
        )
        
    db_user = TestDB(
        # user
        user_id=test.user_id,
        # details
        name=test.name,
        description=test.description,
        # service
        created_by=user.email,
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Unable to create test: f{e}"
        )
    return db_user

@router.get("/id/{test_id}", response_model=TestWithDetail)
async def get_item(test_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TestDB)
        .filter(TestDB.id == test_id)
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Unable to find test with id '{test_id}'")
    return category


@router.put("/update/{test_id}", response_model=TestWithDetail)
async def update_item(test_id: int, test_update: Test, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TestDB)
        .where(TestDB.id == test_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(status_code=404, detail=f"Unable to find test with id '{test_id}'")
    
    # Update fields that are not None
    for key, value in test_update.dict(exclude_unset=True).items():
        setattr(config, key, value)
        
    try:
        await db.commit()
        await db.refresh(config)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Unable to update test {e}")
    return config

@router.get("/list", response_model=List[TestWithDetail])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestDB))
    return result.scalars().all()
