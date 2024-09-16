https://stackoverflow.com/questions/45995530/manpath-cant-set-the-locale-make-sure-lc-and-lang-are-correct
sudo echo "LC_ALL=en_US.UTF-8" >> /etc/environment
sudo echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
sudo echo "LANG=en_US.UTF-8" > /etc/locale.conf
sudo locale-gen en_US.UTF-8

https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e

pg_config = PGConfig("localhost", "5432", "thetadelta", "new_password", "cex")

lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
