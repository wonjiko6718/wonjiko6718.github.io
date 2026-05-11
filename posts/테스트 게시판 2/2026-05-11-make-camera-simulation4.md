---
title: 언리얼 엔진 카메라 시뮬레이션 구현 4
date: 2026-05-11
category: UnrealEngine, UnrealC++, OpenCV, C++
---
사용 환경 기재
| Env/Tools | Version |
|------|------|
| CPU | AMD Ryzen 9 9950X3D2 Dual Editon |
| GPU | NVIDIA GeForce RTX 4090 |
| RAM | 64GB |
| Unreal Engine | 5.3.2-realese Source Build |
| Visual Studio | 2022 Communitiy |

# 경험한 Unreal Engine 빌드 시 오류

## MSVC / VS 버전 불일치 문제 : Engine 버전별 MSVC 버전 지정

Engine - Saved - BuildConfiguration.xml에 다음 구문 추가

```xml
  <WindowsPlatform>
    <Compiler>VisualStudio2022</Compiler>
    <CompilerVersion>14.34.31933</CompilerVersion>
    <ToolchainVersion>14.34.31933</ToolchainVersion>
  </WindowsPlatform>
```

## 상수 산술 연산 오버플로우 : 오류가 난 INFINITY 매크로를 다음으로 교체
```C++
std::numeric_limits<float>::infinity()
```