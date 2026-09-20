# 모두의 수학 Docker 실행 방법

처음에는 아래 순서대로 진행하면 됩니다.

## 1. Docker Desktop 실행

Windows 시작 메뉴에서 **Docker Desktop**을 실행합니다.

또는 PowerShell에서:

```powershell
docker desktop start
```

Docker Desktop 화면에 **Engine running**이 표시되면 준비가 된 것입니다.

---

## 2. Docker가 정상인지 확인

PowerShell에서:

```powershell
docker info
```

정상적으로 Docker 정보가 출력되면 다음 단계로 넘어갑니다.

처음 설치한 경우에는 다음 명령도 한 번 실행해 보는 것이 좋습니다.

```powershell
docker run --rm hello-world
```

`Hello from Docker!`가 나오면 정상입니다.

---

## 3. 모두의 수학 프로젝트 실행

프로젝트 폴더로 이동합니다.

```powershell
cd C:\projects\modu_math
```

Docker 컨테이너를 빌드하고 실행합니다.

```powershell
docker compose up --build -d
```

처음 실행할 때는 필요한 파일을 내려받고 빌드하기 때문에 시간이 조금 걸릴 수 있습니다.

---

## 4. 실행 상태 확인

```powershell
docker compose ps
```

다음 두 서비스가 실행 중인지 확인합니다.

* `web` → Django 웹서버
* `db` → PostgreSQL 데이터베이스

상태가 `Up` 또는 `healthy`이면 정상입니다.

---

## 5. 문제 데이터 동기화

Docker가 정상적으로 실행된 후 다음 명령을 실행합니다.

```powershell
docker compose exec web python manage.py sync_problems
```

이 명령은 모두의 수학 문제 데이터를 데이터베이스에 등록합니다.

> 주의
> `web` 컨테이너가 실행되기 전에 이 명령을 입력하면 오류가 발생합니다.
> 반드시 먼저 `docker compose up --build -d`를 실행해야 합니다.

---

# 웹 에디터 접속

Chrome이나 Edge에서 다음 주소를 엽니다.

### Konva 웹 에디터

```text
http://localhost:8000/editor-konva/
```

또는 아래 주소로 접속해도 됩니다.

```text
http://localhost:8000/
```

자동으로 웹 에디터로 이동합니다.

### 기존 에디터

```text
http://localhost:8000/editor/
```

### 문제 API

```text
http://localhost:8000/api/v1/problems/
```

---

# 평소에는 이렇게만 실행하면 됩니다

Docker 설치와 초기 설정이 끝났다면 앞으로는 대부분 아래 4단계만 하면 됩니다.

```powershell
docker desktop start

cd C:\projects\modu_math

docker compose up -d

docker compose ps
```

그 후 브라우저에서:

```text
http://localhost:8000/
```

를 열면 됩니다.

---

# 에디터 코드를 수정했을 때

`src\modu_math_web\editor_next`의 코드를 수정했다면 프론트엔드를 다시 빌드합니다.

```powershell
cd C:\projects\modu_math\src\modu_math_web\editor_next

npm run build
```

다시 프로젝트 루트로 이동합니다.

```powershell
cd C:\projects\modu_math
```

Docker 이미지를 다시 빌드합니다.

```powershell
docker compose up --build -d
```

---

# 문제가 생겼을 때

## Docker 엔진이 실행되지 않는 경우

먼저 WSL을 종료합니다.

```powershell
wsl --shutdown
```

Docker Desktop을 다시 시작합니다.

```powershell
docker desktop restart
```

그 다음 확인합니다.

```powershell
docker info
```

---

## 웹사이트가 열리지 않는 경우

컨테이너 상태를 확인합니다.

```powershell
docker compose ps
```

로그도 확인할 수 있습니다.

```powershell
docker compose logs -f web
```

종료하려면 `Ctrl + C`를 누릅니다.

---

# Docker 종료

모두의 수학 Docker 환경을 완전히 종료하려면:

```powershell
cd C:\projects\modu_math

docker compose down
```

---

# 가장 중요한 명령 5개

평소에는 이것만 기억해도 됩니다.

```powershell
cd C:\projects\modu_math

docker compose up -d

docker compose ps

docker compose exec web python manage.py sync_problems

docker compose down
```

### 한 줄로 이해하면

**Docker Desktop 실행 → 모두의 수학 실행 → 상태 확인 → 브라우저 접속**

```text
Docker Desktop
      ↓
docker compose up -d
      ↓
docker compose ps
      ↓
http://localhost:8000/
```
