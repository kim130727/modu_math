
1. 시작 메뉴에서 Docker Desktop을 실행합니다.

또는 PowerShell에서:

```powershell
docker desktop start
```

2. Docker Desktop 화면에 `Engine running`이 표시될 때까지 기다립니다.

3. 상태를 확인합니다.

```powershell
docker desktop status
docker info
docker run --rm hello-world
```

4. `hello-world`가 성공한 다음 프로젝트를 실행합니다.

```powershell
cd C:\projects\modu_math
docker compose up --build -d
docker compose ps
```

5. `web`과 `db`가 실행 중이면 문제를 동기화합니다.

```powershell
docker compose exec web python manage.py sync_problems
```

Docker Desktop을 실행했는데도 엔진이 시작되지 않으면 다음 순서로 재시작합니다.

```powershell
wsl --shutdown
docker desktop restart
```

그 후 다시 `docker info`를 확인하세요. 현재 `sync_problems` 명령이 실패하는 것은 `web` 컨테이너가 아직 만들어지지 않았기 때문에 정상적인 결과입니다. 먼저 `docker compose up`이 성공해야 합니다.