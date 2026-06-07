---
title: 언리얼 엔진 Server Move 오류 해결
date: 2026-05-25
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

# 멀티플레이 게임 Character - Controller 구현 중 Movement가 반영되지 않는 현상

## 문제 : Character의 Movement를 Server-Implement 형식으로 구현 후 Controller에서 호출

최초에 멀티플레이를 위한 Movement 호출 메서드를 Server-Implement 형식으로 구현함.

.h
```C++
UFUNCTION(Server, Reliable)
void ServerCallMove(const FVector2D& MovementVector);
```

.cpp
```C++
void ATopdownCharacterBase::ServerCallMove(const FVector2D& MovementVector)
{
	const FVector ForwardDirection = FVector(1.f, 0.f, 0.f);
	const FVector RightDirection = FVector(0.f, 1.f, 0.f);

	AddMovementInput(ForwardDirection, MovementVector.Y);
	AddMovementInput(RightDirection, MovementVector.X);
}
```

## 원인 파악 : 언리얼의 CharacterMovementComponent(이하 CMC)가 가지고 있는 자체 복제 시스템과의 충돌

언리얼의 캐릭터 무브먼트는 자체적인 클라이언트-서버 동기화 메커니즘을 이미 내장한 상태임.

클라이언트 입력 → CMC Local Prediction → 서버에 Move 전송 → 서버 Validation → 결과 클라이언트에 보정

이 과정은 CMC 내부에서 자동으로 처리되도록 진행됨.

UFUNCTION(Server) 매크로를 통해 서버에서만 호출되도록 작성했으므로, CMC의 Prdiction 루프와 분리되게 됨, 따라서 클라이언트가 로컬 예측 없이 서버 결과만 기다리게 되어 끊기게 됨.
CMC가 기대하는 정상 흐름은 다음과 같음.

[Client] AddMovementInput() 호출\
     ↓\
CMC가 자동으로 ServerMove RPC 전송\
     ↓\
[Server] CMC가 검증 및 위치 업데이트\
     ↓\
[Client] 보정값 수신 및 위치 조정

여기서 직접 만든 Server RPC로 우회하는 방식이므로, 이 루프가 깨짐.
ServerRPC의 실행 조건은 클라이언트가 호출하고, 이를 서버에서 실행하는 구조인데,
1. 서버에서 직접 호출할 경우 로컬 실행으로 동작 혹은 무시
2. NetOwner가 없는 경우 RPC 자체가 Drop

## 문제 해결 : 언리얼의 CMC가 가지는 자체 복제 시스템으로 인가, 기본 메서드 형식으로 변경

언리얼의 CMC가 가지는 자체 복제 시스템을 이용하고, 기본 메서드를 호출하는 형식으로 변경함.

.h
```C++
void CallMove(const FVector2D& MovementVector);
```

.cpp
```C++
void ATopdownCharacterBase::CallMove(const FVector2D& MovementVector)
{
	const FVector ForwardDirection = FVector(1.f, 0.f, 0.f);
	const FVector RightDirection = FVector(0.f, 1.f, 0.f);

	AddMovementInput(ForwardDirection, MovementVector.Y);
	AddMovementInput(RightDirection, MovementVector.X);
}
```
기본 메서드로 변경 후, 정상적인 Movement를 확인하며 마무리함.