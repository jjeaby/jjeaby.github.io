# XPS15 For Ubuntu



* XPS15 의 경우 우분투 설치가 잘되기로 잘 알려져 있다. 하지만, XPS 15 9560 의 경우 Ubuntu 를 설치하면 배터리 시간이 너무 짧다는 문제가 생긴다 


* 이런 문제를 해결하기 위해서는 **1050 그래픽 카드를 필요한 경우애만 활성화하고 기본적으로 Intel 내장 그래픽 카드를 사용**하는 것이다.
>  **이렇게 설정하여 사용 하면 XPS15 9560 모델을 산 이유가 많이 사라진다구구매전 Ubuntu 를 사용한 것이라면 다시 한번 고민 할 필요가 있다**

* XPS 15 9560 모델의 Ubuntu 설치 방법은 다음과 같다



<br>
<br>

## 설치 방법 
1. Ubuntu 설치 USB 만들기  
 . 우분투 설치 USB 는 ubuntu(https://www.ubuntu.com/download)에서 16.04 LTS 버전으로 만든다 


2. XPS 부팅시 F12 버튼을 눌러 진입한 Bios 설정에서 **Secure Boot 를 Disable** 로 설정하고 저장한다 


3. Ubuntu USB 를 연결하고 F12 버튼을 눌려 UEFI Boot 옵션에 나타난 USB 를 선택한다 


4. Ubuntu boot 에서 Install Ubuntu 메뉴를 선택하고 설치를 진행한다 
 . 설치는 Default 옵션으로 설치하면 된다


5. Ubuntu 설치 후에는 Kernel 업데이트, Nvidia 그래픽 드라이버 설치, 배터리 관리 App 설치 등과 같
은 작업을 수행하면 된다.


  > A. **Kernel 업그레이드**

```java
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.13/linux-headers-4.13.0-041300_4.13.0-041300.201709031731_all.deb
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.13/linux-headers-4.13.0-041300-generic_4.13.0-041300.201709031731_amd64.deb
wget http://kernel.ubuntu.com/~kernel-ppa/mainline/v4.13/linux-image-4.13.0-041300-generic_4.13.0-041300.201709031731_amd64.deb
sudo dpkg -i *.deb

sudo vi /etc/default/grub

# GRUB_CMDLINE_LINUX_DEFAULT 를 아래와 같이 수정 
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash acpi_rev_override=1"
```


  > B. **Intel 그래픽 드라이버 설치**

sudo bash -c "$(curl -fsSL http://bit.ly/IGFWL-install)"
  
  > C. **Nvidia 그래픽 드라이버 설치**

sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

  > D. **Ubuntu 드라이버 인스톨**

sudo ubuntu-drivers autoinstall


  > E. **Nvidia Prime Profile 설정**
 
sudo prime-select intel - 

```java
내장 intel 그래픽 카드를 사용 하도록 설정하고 리부팅한다 
(1050 글픽 카드가 필요한 경우 sudo prime-select nvidia 명령어를 실행함됨)
xwindow 서비스를 리스타트하거나 리부팅을 하면 설정이 적용된다 
```


  > F. **배터리 관련 App 설치**
 
```
sudo apt-get install tlp tlp-rdw powertop
 > 배터리 관련 A설치 

sudo tlp start

sudo powertop --calibrate

sudo powertop --auto-tune  

``` 
