# 🐧 æ-PENGUINJEAN
<p align="center">
    <img src="https://img.shields.io/badge/python-3.8+-3776AB?logo=python">
    <img src="https://img.shields.io/badge/discord.py-2.7.1-5865F2?&logo=discord">
</p>

<p align="center">
    <strong>"서버의 모든 순간을 기록하고, 관리의 품격을 높이다."</strong><br>
    **æ-PENGUINJEAN**은 정교한 로깅과 강력한 관리 기능을 제공하는 Discord 봇입니다.
</p>

<p align="center">
    <a ""><strong>[ ➔ 봇 초대하기 ]</strong></a>
</p>

---

## ✨ 주요 기능

### 🛡️ 서버 관리 (Moderation)
* **음성 제재**: 마이크 차단(`mute`), 헤드셋 차단(`deafen`), 음성 채널 강제 퇴장(`vckick`) 기능을 지원합니다.
* **유연한 제재**: 타임아웃, 추방, 차단 기능을 제공하며 이름이나 ID를 통한 차단 해제(`unban`)가 가능합니다.
* **스마트 타이머**: `10m`(분), `1h`(시간), `1d`(일) 등 직관적인 시간 단위를 해석하여 자동 처벌 해제를 수행합니다.

### 📝 로깅 시스템 (Logging)
* **메시지 이벤트**: 메시지 수정 및 삭제 시 이전 내용을 포함하여 기록합니다.
* **유저 유입/유출**: 멤버의 입장과 퇴장을 실시간으로 추적하여 기록합니다.
* **음성 상태 모니터링**: 채널 이동, 입장, 퇴장 등 음성 채널 내 모든 변화를 감지합니다.
* **로그 분리**: 일반 로그와 처벌 로그 채널을 각각 분리하여 관리 효율성을 높였습니다.

### 🎫 문의 및 지원 (Ticket System)
* **하이브리드 티켓 생성**: `!open` 명령어와 **버튼 클릭** 방식을 모두 지원하여 상황에 맞는 문의 접수가 가능합니다.
* **프라이빗 채널**: 문의 생성 시 관리자와 요청자만 접근 가능한 전용 채널이 생성되어 안전한 상담을 보장합니다.
* **자동 관리**: 상담 종료 후 `!close`를 통해 채널 정리와 기록 관리를 간편하게 수행할 수 있습니다.

### ⚙️ 설정 (Settings)
* **서버별 커스텀**: 각 서버마다 독립적인 채널 설정(`log`, `punish`, `bot`)을 `config.json`에 영구 저장합니다.
* **자동 채널 관리**: 명령어 실행 후 사용자 메시지를 자동 삭제하여 대화 흐름을 방해하지 않습니다.

## 🚀 시작하기

### 필수 조건
* Python 3.8 이상
* [Discord Developer Portal](https://discord.com/developers/applications)에서 발급받은 봇 토큰

### 설치 및 실행
```bash
# 저장소 복제
git clone https://github.com/penguinjean0421/ae-PenguinJean.git
cd ae-PenguinJean

# 필수 라이브러리 설치
pip install -r requirements.txt

# 설정 파일 작성
cp .env.example .env
# .env 파일을 열어 BOT_TOKEN과 API_KEY를 입력하세요.

# 봇 실행
python main.py
```

## 📋 명령어 요약 (Commands)

기본: `!`(설정 시 다중 접두사 지원)

### 관리 및 설정
| 카테고리 | 명령어 | 설명 |
| :---: | :---: | :---: |
| 정보 |`!help`, `!credit` | 기능 안내 및 제작자 정보 확인 |
| 설정 | `!set [server/punish/bot/emoji/ticket] [#채널]` | 용도별 전용 채널 설정 |
| 초기화 | `!reset [server/punish/bot/all]` | 특정 설정 초기화 또는 전체 서버 데이터 삭제 |

### 제재 (Moderation)

| 명령어 | 대상 | 시간/사유 예시 |
| :---: | :---: | :---: |
|`!mute` | `@유저` | `10m` (마이크 차단) |
|`!timeout` | `@유저` | `30m 사유` (채팅 금지) |
|`!kick` / `!ban` | `@유저` | `사유`(서버 추방/차단) |
|`!unban` | `이름#태그` 또는 `ID` | 차단 목록에서 찾아 해제 |

### 티켓 (Ticket)
| 명령어 | 설명 |
| :---: | :---: | 
| `!open` | 티켓 채널 생성 |
| `!close` | 티켓채널 닫기 |
| `!answer [답변내용]` | 답변 내용 임베드로 전송 |


### 💡 기술적 지원 및 문의
서비스 이용 중 발생하는 버그 제보나 기능 제안은 [공식 서포트 서버]()를 이용해 주세요.

## 파일 구조
```
.
├── cogs/                 # 봇의 기능별 모듈 (Cog 구조로 확장성 확보)
│   ├── information.py    # 도움말 출력 및 봇 정보(Credit) 제공
│   ├── logger.py         # 메시지/멤버/음성 상태 변화 실시간 로깅 리스너
│   ├── moderation.py     # 제재 로직(Time-parsing 포함) 및 관리 명령어
│   ├── settings.py       # JSON 기반 서버별 설정 데이터 핸들링
│   └── ticket.py         # 버튼 기반 1:1 문의 티켓 생성 및 채널 관리 자동화
├── .env                  # API 토큰 및 환경 변수 관리 (보안 정보 분리)
├── config.json           # 서버별 커스텀 설정 데이터 영구 저장 (자동 생성)
├── main.py               # 봇 클래스 정의, Cog 로드 및 메인 진입점
└── requirements.txt      # 프로젝트 실행을 위한 의존성 라이브러리 목록
```

## 👨‍💻 제작자
* Developer: penguinjean0421
    * GitHub: [penguinjean0421](https://github.com/penguinjean0421)
* Contact
    * E-Mail : [penguinjean0421@gmail.com](mailto:penguinjean0421@gmail.com)
    * Discord : [@penguinjean0421](https://discord.com/users/penguinjean0421)

<p align="center"><strong>Need Help?</strong> <a href="">Support Server</a> | <a href="https://github.com/penguinjean0421/ae-PenguinJean">Documentation</a> | <a href="mailto:penguinjean0421@gmail.com">Contact</a>
</p>