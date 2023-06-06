# Firebase's insecure rules scanner

Firebase's insecure rules scanner is a tool made for hackers and android developers. It extracts the Firebase URL from an apk and checks to see if it's vulnerable or has permissions correctly added to it.


## Installation
Install it manually, by running these commands 

```bash

git clone https://github.com/cTFk1ller/firebase-mapping.git
cd firebase-mapping
pip3 install -r requirements.txt


```

## Usage

```python
# Check if this app contains a Firebase URL.
python3 main.py -a APK_PATH 

# Use the -o option to save JSON data into a file.
python3 main.py -a APK_PATH -o OUTPUT

# Use --apk or --url; don't use both; use the -q option to run in quiet mode.
python3 main.py --url FIREBASE_URL -q

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[cTFk1ller](https://github.com/cTFk1ller)
