from freedomserver.configuration.smtp_config import SmtpConfig

RICKY_SANCHEZ_NICK: str = "@ricky.sanchez.64"
MORTY_NICK: str = "morty.45"

RICKY_SANCHEZ_PHONE: str = "+5564999999999"
MORTY_PHONE: str = "+5545999999999"

RICKY_SANCHEZ_ACI: str = "0192d38d-ce22-7276-8fbd-008fc4aedb54"
MORTY_ACI: str =  "0192d38d-ce23-761b-b1ce-26546c1c1256"

RICKY_SANCHEZ_EMAIL: str = "ricky.sanchez@freedom.mail"
MORTY_EMAIL: str = "morty@freedom.mail"

RICKY_SANCHEZ_PIN_HASH: str = "iamafakerickysanchezdigest"
MORTY_PIN_HASH: str = "iamtruemortydigest" 

ED25519_PUBLIC_KEY: str = "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEA+7HCNQc9INV1bxdf40+zuprCjA6KlpHr/hlN0S2BdT0=\n-----END PUBLIC KEY-----"
ED25519_PRIVATE_KEY: str = "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEILdorxBzj9e6DK7n3wMvqo9r/NjbmB4K/kkJlOUOTyap\n-----END PRIVATE KEY-----"

X25519_PUBLIC_KEY: str = "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VuAyEAwzhbusC7X9aNcLHacoVMykmgjR2161SL+r195wAyqWc=\n-----END PUBLIC KEY-----"

SMTP_CONFIG: SmtpConfig = SmtpConfig(
    host="test_host",
    port="test_port",
    user="test_user",
    password="test_password"
)

SERVER_PUBLIC_KEY: str = "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAoVQWbQbvR1XyCvxxyCPeuVVNGX+3An/HRKJNrzHXblM=\n-----END PUBLIC KEY-----"

SERVER_PRIVATE_KEY: str = "-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEIJGX+J198uswHpxK8Cz6e4HEx26UxeOcm3oaHpKmn/bQ\n-----END PRIVATE KEY-----"