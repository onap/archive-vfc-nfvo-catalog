@REM
@REM
@REM Copyright 2016 [ZTE] and others.
@REM
@REM Licensed under the Apache License, Version 2.0 (the "License");
@REM you may not use this file except in compliance with the License.
@REM You may obtain a copy of the License at
@REM
@REM     http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM Unless required by applicable law or agreed to in writing, software
@REM distributed under the License is distributed on an "AS IS" BASIS,
@REM WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM See the License for the specific language governing permissions and
@REM limitations under the License.
@REM

@echo off
set HOME=%~dp0
set user=%1
set password=%2
set port=%3
set host=%4
echo start init catalog db
echo HOME=%HOME%
cd /d %HOME%
mysql -u%user% -p%password% -P%port% -h%host% < %HOME%\dbscripts\mysql\openo-common_tosca-catalog-createobj.sql
set "err=%errorlevel%"
if "%err%"=="0" (
   echo init catalog db success
  ) else (
    echo failed init catalog db
    pause
  )