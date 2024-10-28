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

ED25519_KEY: str = "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAvpD/RP1BKRukhpic4tA13HQNpXIOU3GP/gfEYbxQMxU=\n-----END PUBLIC KEY-----"
X25519_KEY: str = "-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VuAyEAwzhbusC7X9aNcLHacoVMykmgjR2161SL+r195wAyqWc=\n-----END PUBLIC KEY-----"

SMTP_CONFIG: SmtpConfig = SmtpConfig(
    host="test_host",
    port="test_port",
    user="test_user",
    password="test_password"
)