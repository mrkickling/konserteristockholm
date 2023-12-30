FROM php:8-apache

RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

COPY web/ /var/www/html/