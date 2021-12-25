# Update Vulnman Server
To update `vulnman` you just need to follow the steps in this section.

Update the codebase:

```bash
git pull
```

You should check the [settings file](../configuration/index.md) for new settings you need to apply.

Get the new database changes:

```bash
python manage.py migrate
```
