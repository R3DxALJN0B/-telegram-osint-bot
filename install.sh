
#!/bin/bash

# تحديث النظام
sudo apt update && sudo apt upgrade -y

# تثبيت المتطلبات الأساسية
sudo apt install -y python3 python3-pip git curl

# إنشاء مجلد للأدوات
mkdir -p osint-tools && cd osint-tools

# تثبيت Sherlock
git clone https://github.com/sherlock-project/sherlock.git
cd sherlock
pip3 install -r requirements.txt
cd ..

# تثبيت theHarvester
git clone https://github.com/laramies/theHarvester.git
cd theHarvester
pip3 install -r requirements/base.txt
cd ..

# تثبيت PhoneInfoga
git clone https://github.com/sundowndev/phoneinfoga.git
cd phoneinfoga
pip3 install -r requirements.txt
cd ..

# تثبيت Holehe
git clone https://github.com/megadose/holehe.git
cd holehe
pip3 install -r requirements.txt
cd ..

# تثبيت Socialscan
git clone https://github.com/iojw/socialscan.git
cd socialscan
pip3 install -r requirements.txt
cd ..

# تثبيت EmailRep (ما يحتاج تحميل، مجرد استخدام API)

# Skymem و Username-Search.org سيتم استخدامهم عبر requests من البوت مباشرة (ما يحتاج تثبيت)

# العودة للمجلد الرئيسي
cd ..

# تثبيت متطلبات البوت لو فيه ملف requirements.txt
if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
fi

echo "تم تثبيت جميع الأدوات بنجاح!"
