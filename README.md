# Bot de Exploits e Notificações de Segurança

Este é um bot Telegram que permite aos usuários buscar vulnerabilidades usando o CVE (Common Vulnerabilities and Exposures) e receber notificações sobre vulnerabilidades de segurança recentes.

## Funcionalidades
- **/exploit `<CVE-ID>`**: Busca detalhes de uma vulnerabilidade específica por ID, incluindo descrição e referências.
- **/recent**: Retorna uma lista das vulnerabilidades mais recentes disponíveis.
- **/start**: Exibe uma mensagem de boas-vindas e instruções de uso.

---

## Como Criar um Bot e Obter um Token

Para usar este bot, você precisa criar o seu próprio bot no Telegram e obter o token de acesso. Siga os passos abaixo:

1. **Acesse o Telegram** e procure pelo bot chamado [BotFather](https://t.me/BotFather).
2. **Inicie uma conversa com o BotFather** enviando `/start`.
3. **Crie um novo bot** enviando o comando `/newbot` e siga as instruções fornecidas. Você precisará escolher um nome e um nome de usuário para o seu bot.
4. Após criar o bot, o BotFather fornecerá um **Token de API**. O token terá um formato parecido com este: `123456789:ABCdefGhIJKlmnOPqRsTuVWXyz`.

### Como Usar o Token no Código
Substitua `YOUR_TELEGRAM_BOT_TOKEN` no código pelo token que você obteve do BotFather:
```python
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
```

---

## Como Executar o Bot

#### 1. Clonar o Repositório
```bash
git clone https://github.com/cleissonbarbosa/telegram-security-bot
cd telegram-security-bot
```

#### 2. Instalar Dependências:
Certifique-se de que você tenha o Python instalado e então execute:
```bash
pip install -r requirements.txt
```

#### 3. Executar o Bot: 
Após configurar o token e instalar as dependências, você pode rodar o bot com o seguinte comando:
```bash
python src/main.py
```

---

## Melhorias Futuras

- [ ] Adicionar suporte para pesquisar vulnerabilidades por palavras-chave.
- [ ] Notificações automáticas de vulnerabilidades em intervalos definidos.
- [ ] Integração com outras APIs de segurança.
- [ ] Filtros avançados para buscas de CVE.

---

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests com sugestões ou melhorias.

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.