---
title: 언리얼 엔진 네트워크 관련 개념 정리 - Server, Client와 변수 복제 개념
date: 2026-06-07
category: UnrealEngine, UnrealC++
---
사용 환경 기재
| Env/Tools | Version |
|------|------|
| CPU | AMD Ryzen 9 9950X3D2 Dual Editon |
| GPU | NVIDIA GeForce RTX 4090 |
| RAM | 64GB |
| Unreal Engine | 5.3.2-realese Source Build |
| Visual Studio | 2022 Communitiy |

# 멀티플레이 구현 중 네트워크 관련 개념 정리 - Server, Client의 역할, 변수 복제 개념

## 언리얼에서 기대하는 네트워크 흐름

언리얼에서 제공하는 Dedicated Server, 이를 구현하기 위해 사용하는 Replication, RPC(Remote Procedure Call)의 개념은 다음과 같은 역할을 기대함.

[Server](언리얼 엔진으로 빌드된 Dedicated Server 혹은 Listen Server 역할의 호스트)
- GameMode 등 게임플레이 전반에 관한 로직의 수행, 전체 흐름에 대한 관리 주체.
- 클라이언트의 행위에 대한 연산 요청을 받아 결과를 반환하며, 이를 각 클라이언트에게 알림.\
    Replication = 상태 변화에 따른 변수의 자동 동기화\
	Client RPC = 이벤트 콜 등 상황 변화에 따른 함수를 특정 클라이언트에게 전달\
	Multicast RPC = 이벤트 콜 등 상황 변화에 따른 함수 결과를 모든 클라이언트에게 전달

[Client](언리얼 엔진으로 빌드된 클라이언트)
- 네트워크 환경에 접속해 플레이를 수행하는 유저.
- 행위의 전반에 대해 서버에 요청을 보내고, 결과를 반환하여 나의 환경에 반영함.\
	Server RPC = 이벤트 콜 등 상황 변화에 따른 함수를 서버에게 요청하여 동기화

즉, 클라이언트는 입력에 대한 연산을 서버에게 요청 → 서버는 이를 받아 처리하고 결과를 클라이언트에게 알림 → 클라이언트는 이를 반영
클라이언트는 [내가 이런 행위를 수행했다], 서버는 [그 행위의 결과는 이것이다] 라고 정리가 가능함.

+ 여기서 헷갈렸던 개념으로, Server와 Client RPC 선언은 실행 주체가 반대임을 확인해야 한다. Server매크로는 클라이언트가 서버에게 요청, Client 매크로는 서버가 반환하는 구조임을 유의한다.

## 네트워크 구성을 위한 언리얼 제공 매크로 옵션

매크로 옵션에 관한 이해를 돕기 위해, 플레이어가 달리는 행위에 대한 네트워크 환경을 가정하고 작성한다.

### UPROPERTY(변수) 관련 옵션

1. 변수의 Replicated 옵션, GetGetLifetimeReplicatedProps 오버라이드 형식

.h
```C++

virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

UPROPERTY(Replicated)
bool bIsRunning;

```

.cpp
```C++
ASampleActor::ASampleActor()
{
	bReplicates  = true;
}

void ASampleActor::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(ASampleActor, bIsRunning);
}
```

2. ReplicatedUsing 형식

.h
```C++

virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

UPROPERTY(ReplicatedUsing = OnRep_Health) // 서버가 변수를 바꾸고, 그 변화가 나에게 도착했을때 다음 함수 실행, 즉 클라이언트의 상태변화에 따른 콜백 자동화
bool bIsRunning;

UFUNCTION()
void OnRep_IsRunning(); //클라이언트가 부를 함수 선언
```

.cpp
```C++
ASampleActor::ASampleActor() // 레플리케이션 옵션은 동일하게 켜져있어야 함.
{
	bReplicates  = true;
}
void ASampleActor::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const // 해당 변수를 복제하기 위해 동일하게 필요함.
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(ASampleActor, bIsRunning);
}
void ASampleActor::OnRep_IsRunning()
{
	if(bIsRunning)
	GetCharacterMovement()->MaxWalkSpeed = 600.0f; // 클라이언트가 서버의 변화를 수신했다면, 조종 대상 캐릭터의 걷는 속도에 변화를 반영함.
}
```

상위와 같이 구현이 가능하다. 그런데 여기서 ReplicatedUsing 형식을 사용했다면, 이 함수가 "클라이언트"에서 실행되는 함수임을 알아야 한다.
따라서 서버에서 자체적으로 처리할 함수가 필요하다.
서버는 자체적으로 bIsRunning의 변화에 대응할 함수가 동일하게 필요하다.

따라서 네트워크 환경에서 변수에 대응한 무언가를 구현할 경우에는, 다음 순서대로 진행하면 된다.\
(공통 - 복제 기본 세팅)\
	- bReplicates = true\
	- UPROPERTY(Replicated) 혹은 UPROPERTY(ReplicatedUsing = 함수) ← Replicated 옵션을 포함한다. 하나만 선언.\
	- GetLifetimeReplicatedProps 변수 등록

(변화에 반응하는 이벤트)\
	- 클라이언트 : ReplicatedUsing을 사용했다면 OnRep 형식의 콜백 함수에서 구현해 반영\
	- 서버 : 변수를 변경하는 함수를 선언하고 구현해 동일하게 처리

