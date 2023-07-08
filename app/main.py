from fastapi import FastAPI

# main router
app = FastAPI(title="FITMATE API", version=0.1)

# root 
@app.get(path="/",tags=["Root Route"])
def read_root():
    """
    read the root of the api
    :return : status of the api
    """
    return {"status":"OK","message":"Available to integrate"}