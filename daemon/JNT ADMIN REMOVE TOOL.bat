@shift /0
@ECHO OFF 
title jibtech ADMIN CONTROL REMOVE TOOL
color 8f 
cls
:menu
echo                 %TIME%
echo                 %DATE%
echo.
echo  = ===========================================================================                       
echo  =                                                 =
echo. =                         jibtech technologies                                                  =
echo  =      =
echo. =                                                                           =
echo  = ===========================================================================
echo.
echo.
echo   .Install Correct adb drivers on your Pc   
echo.  .Connect phone on PC
echo.  .Enable usb debug In your Phone
echo.  .Type 1 and then press Enter
echo.
echo                        moto                     Contact Us
echo                        mdm                    telegram:@server
echo                    
echo.
set /p m=      Enable Usb Debug On Phone, Connect The Phone. Type 1 Then Enter..
cls
if %M%==1 goto 1
if %M%==2 goto 2

:1
adb shell pm uninstall -k --user 0 com.google.android.apps.work.oobconfig.channel
pause
goto :menu

:2
pm list packages -s
pause
goto :menu
