from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post('/register')
async def register_user():
    return {'message': 'User registered'}

@router.post('/login')
async def login_user():
    return {'message': 'User logged in'}

@router.get('/timeline')
async def get_timeline():
    return {'message': 'Timeline'}

@router.post('/song')
async def add_song():
    return {'message': 'Song added'}
