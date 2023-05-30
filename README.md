# Firebase-Mapping

Firebase mapping is a tool made by and for hackers. Extract the Firebase URL from an apk and check to see if it's vulnerable or has permissions. like deleting, adding, or querying records. I am not responsible for any misuse.

## Installation
Install it manually, by running these commands 

```bash

 git clone https://github.com/cTFk1ller/firebase-mapping.git
 cd firebase-mapping
 pip3 install -r requirements 


```

## Usage

```python
# dump databases 
python3 main.py --url FIREBASE_URL -D 

# dump tables 
python3 main.py --url FIREBASE_URL -d DATABASE_NAME -T  

# dump records 
python3 main.py --url FIREBASE_URL -d DATABASE_NAME -t tablename -P 

# dump records into a file 
python3 main.py --url FIREBASE_URL -d DATABASE_NAME -t tablename -P --output FILENAME

# run in quite mode 
python3 main.py --url FIREBASE_URL -d DATABASE_NAME -t tablename -P --output FILENAME -q

# delete record || Replace record with databasename.tablename.columnname.rowdata....etc
python3 main.py --url FIREBASE_URL -r record 

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[cTFk1ller](https://github.com/cTFk1ller)
