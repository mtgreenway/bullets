#  Copyright 2013 Open Cloud Consortium
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import smtplib
import local_settings

server = smtplib.SMTP_SSL(host="authsmtp.uchicago.edu", port=465)
server.login(local_settings.username, local_settings.password)
server.sendmail("mgreenway@uchicago.edu", "mgreenway@uchicago.edu", "test")
