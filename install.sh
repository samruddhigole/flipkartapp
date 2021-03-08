sudo -u postgres createuser flipkartuser -s
sudo -u postgres createdb flipkartuser


echo "FLIPKART\n\n\n\n\n\n" | adduser flipkartuser --quite --disabled-password

./reset.expect flipkartuser "admin123"

sudo -u postgres psql -c "ALTER USER flipkartuser PASSWORD 'admin123';"

sudo -u postgres psql -c "create database flipkartapp;"
