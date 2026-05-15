from fastapi import FastAPI

app = FastAPI()



@app.get('/')
async def root():
    return {"message": "Welcome to Split Expenses API"}

@app.get('/health')
def health_check():
    return {"status": "ok"}

@app.get('/signup')
async def signup():
    return {"message": "Signup"}


@app.get('/login')
async def login():
    return {"message": "Login"}


   
