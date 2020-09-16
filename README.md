**Activate the virtual environment**
Inside the conda prompt
```
conda activate py3-blockchain
```

**Install all the packages**

```
pip install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment
```
python -m pytest backend/tests
```

**Run the application and API**

Make sure to activate the virtual environment

```
python -m backend.app
```

**Run a peer instance**

Make sure to activate the virtual environment

```
set PEER=True
python -m backend.app
```

**Run the frontend**

In the frontend directory:
```
npm run start
```

**Seed the backend with data**

Make sure to activate the virtual environment.

```
set SEED_DATA=True
python -m backend.app
```