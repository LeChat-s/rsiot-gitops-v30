# Rules (SmartHome)

Мини-сервис правил для варианта №30. GET `/` или `/version` возвращает номер сборки
и `message: rules v1`. GET `/health` — проверка готовности.
POST `/evaluate` с JSON `{"temperature":31,"humidity":72,"motion":true}`
возвращает `actions` с действиями для системы «СмартДом».

```powershell
cd app
python -m unittest discover -s tests -v
python server.py
# из второго окна: Invoke-RestMethod http://localhost:8110/version
```

Для демонстрации полного CI/CD измените строку `RELEASE_MESSAGE = "rules v1"`
на `rules v2`, а в тесте `test_version_message` измените ожидаемую строку на `rules v2`.
После push коммит бота обновит тег в `infra/deployment.yaml`, и Argo CD выполнит
автосинк. Не обновляйте Deployment вручную в этом эксперименте.
