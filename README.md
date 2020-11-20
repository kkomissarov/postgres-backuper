python3.6+

Clone repo:
```bash
git clone git@github.com:kkomissarov/postgres-backuper.git
```

Move to project directory:
```bash
cd postgres-backuper
```

Create virtual environment:
```bash
python3 -m venv venv
```

Activate virtual environment:
```bash
source venv/bin/activate
```

Copy `.env` sample to `.env`. Then open `.env` in your favourite text editor 
and configure all environment variables for your db.

```bash
cp .sample.env .env
```


Open crontab file:
```
crontab -e
```

Add new task and save file. Set full path for your python interpreter in virtual env.
For example, this command will backup your db every 12 hours:
```bash
0 */12 * * * /home/user/db-backuper/venv/bin/python main.py
```

