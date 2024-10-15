#!/bin/bash



if [ -f .env ]; then
    export cert_folder=$(grep '^cert_folder=' .env | cut -d'=' -f2 | tr -d ' ')
    export pki_host=$(grep '^pki_host=' .env | cut -d'=' -f2 | tr -d ' ')
else
    echo "Errore: file .env non trovato nella cartella corrente."
    exit 1
fi

# Debug: stampa i valori di server_host e cert_folder
echo "cert_folder: $cert_folder"

CSR_FILE="testpier.csr"
KEY_FILE="pre_enrolment.key"
CERT_FILE="pre_enrolment.crt"
PKI_ENDPOINT="https://$pki_host/.well-known/est/simpleenroll"
OUTPUT_CERT_FILE="src/$cert_folder/client_fake.crt"

if [ ! -d "src/$cert_folder" ]; then
    echo "Errore: La directory 'src/$cert_folder' non esiste."
    exit 1
fi

# Esegui il comando curl con i parametri hardcodati
curl -v -k -H "Content-Type: application/pkcs10" \
    --data @"$CSR_FILE" \
    --key "$KEY_FILE" \
    --cert "$CERT_FILE" \
    "$PKI_ENDPOINT" | base64 -d | openssl pkcs7 -inform der -print_certs > "$OUTPUT_CERT_FILE"

# Verifica se il comando curl ha avuto successo
if [ $? -eq 0 ]; then
    echo "Certificato salvato con successo in $OUTPUT_CERT_FILE"
else
    echo "Errore durante l'esecuzione del comando."
    exit 1
fi
