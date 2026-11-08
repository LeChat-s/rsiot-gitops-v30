# RSiOT Lab 7 — rules / OpenTofu / GitOps

Публичный рабочий репозиторий для варианта №30 (StudentID `230203`, GitHub `LeChat-s`).
IaC: **OpenTofu**, приложение: **rules**, namespace: `gitops30`, порт: **8110**, реплики: **3**.

## Компоненты

- `app/`: HTTP-сервис правил SmartHome, 7 модульных тестов, Dockerfile.
- `infra/`: Deployment и Service, которыми управляет Argo CD.
- `.github/workflows/ci.yml`: тесты → SHA-образ в GHCR → коммит нового тега в `infra/`.
- `scripts/update_image.py`: проверенная замена одного image-тега в YAML.
- `argocd/application.yaml`: Application для работы после OpenTofu.
- `demo-infra/`, `demo-application.yaml`: временное демо для первого автосинка.

**Важно:** в `infra/deployment.yaml` изначально стоит тег `:bootstrap`, который ещё не существует.
При первом push каталога `app/` workflow выпустит образ с SHA и автоматически заменит этот тег.
Первый пакет GHCR обычно приватный. После публикации нужно сделать `rules` **Public**
в GitHub → Packages → rules → Package settings → Change visibility, иначе
Kubernetes не скачает образ без imagePullSecret.

## Первый запуск (Windows PowerShell)

1. Установить OpenTofu: `winget install --exact --id OpenTofu.Tofu`.
2. Создать новый kind: `kind create cluster --name gitops-lab`. Существующий `kind-rsiot` не трогать.
3. Установить Argo CD (официальный install.yaml, `--server-side --force-conflicts`).
4. Создать *публичный* репозиторий `LeChat-s/rsiot-gitops-v30`, загрузить туда это содержимое, ветка `main`.
5. Из **учебного** `task_07/src/terraform` выполнить `tofu init`, `tofu plan`, `tofu apply`.
6. Запустить демо в `demo`, снять скриншот Synced/Healthy, удалить демо после эксперимента.
7. Дождаться успешного Actions, сделать GHCR rules Public, применить `argocd/application.yaml`.
8. Убедиться: `kubectl -n argocd get applications`, `kubectl -n gitops30 get deploy,pods,svc`.
9. Запустить `kubectl -n gitops30 port-forward svc/rules 8110:8110`;
   `Invoke-RestMethod http://localhost:8110/version` из второго PowerShell.

## Эксперименты

- **IaC drift:** после `tofu apply` исправить `rules-variant-config` вручную командой
  `kubectl -n gitops30 edit cm rules-variant-config`, затем `tofu plan` показывает diff,
  `tofu apply` возвращает состояние к HCL.
- **Self-heal:** `kubectl -n gitops30 delete deploy rules` → Argo CD возвращает Deployment;
  снять скриншоты до и после, дождаться Synced/Healthy.
- **Revert:** поменять `infra/deployment.yaml` через git (например `replicas: 2`),
  push, дождаться изменения, затем `git revert <sha_bad_commit>` и новый push.
  Argo CD вернёт три реплики. Не меняйте образ на заведомо несуществующий,
  чтобы не получить лишнюю ошибку pull.
- **Full CI:** в `app/server.py` изменить `RELEASE_MESSAGE` на `rules v2`, и в
  `app/tests/test_rules.py` ожидаемую строку на `rules v2`; push, проверить
  Actions → commit бота → Argo CD → `/version` выдаёт `rules v2`, без `kubectl apply`.

Протоколы `plan.txt`, `plan2.txt`, скриншоты UI и цепочки CI должны быть настоящими.
Подробный порядок и команды находятся в учебном `task_07/src/README.md`.
