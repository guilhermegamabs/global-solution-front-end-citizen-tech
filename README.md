# Orienta Saúde

Prova de Conceito CitizenTech da Global Solution 2026/2 (Front-end em Sistemas de IA). O cidadão descreve o que está sentindo e recebe, em linguagem simples, a urgência do caso e o serviço de saúde mais adequado (cuidado em casa, UBS, UPA ou SAMU).

## Problema e público

PREENCHER: quem é afetado, qual a dor concreta e a fonte que sustenta (dado, notícia, relato ou entrevista). Sugestão: superlotação de UPAs e pronto-socorros por casos de baixa complexidade, e dificuldade do cidadão em saber onde buscar atendimento.

## Conta, verificação por e-mail e histórico

- **Cadastro:** e-mail e senha. A conta só passa a valer depois de confirmar um código de 6 números enviado por e-mail (vale 10 minutos, máximo de 5 tentativas, reenvio a cada 60 segundos).
- **E-mail único:** guardado em minúsculas, com restrição `UNIQUE` no banco.
- **Senha:** hash `scrypt` (biblioteca padrão), nunca em texto puro. O código de verificação também fica só como hash (HMAC com `SEGREDOAPP`).
- **Sessão:** token aleatório de 7 dias; só o hash dele vai para o banco, então o logout invalida de verdade.
- **Proteções:** bloqueio de 15 minutos após 5 logins errados, mensagem igual para e-mail inexistente e senha errada, reenvio de código sem revelar se o e-mail existe.
- **Histórico por usuário:** triagem e revisão exigem login e são gravadas no banco. O texto que a pessoa digita não é gravado (minimização de dados, LGPD); guarda-se o resultado da IA, a faixa de idade e a revisão humana.
- **Direito de apagar:** o menu lateral tem "Apagar minha conta", que remove usuário, sessões, códigos e histórico.

### Banco de dados

SQLAlchemy Core com a variável `DATABASEURL`. As tabelas (`users`, `verificationCodes`, `sessions`, `triageRecords`) são criadas na primeira conexão.

| Ambiente | Banco |
|---|---|
| Testes | SQLite em memória |
| Local sem Docker | SQLite em arquivo (`sqlite:///orienta.db`) |
| Docker Compose | PostgreSQL 16 em volume persistente |
| Produção | PostgreSQL no Neon (a URL `postgres://...` é ajustada automaticamente) |

### E-mail (Brevo)

Crie uma conta na Brevo, gere uma chave de API e verifique um e-mail remetente. Preencha `BREVOAPIKEY` e `SENDEREMAIL`. Para desenvolver sem enviar e-mail, use `MOSTRARCODIGONOLOG=true` e o código aparece no terminal da API (nunca use isso em produção).

### Limites conhecidos

- Ao recarregar a página (F5) o Streamlit perde a sessão e a pessoa entra de novo.
- O bloqueio de logins errados fica na memória do processo (zera ao reiniciar e não é compartilhado entre instâncias).
- Sem migrações versionadas: o esquema é criado automaticamente. Para evoluir o banco em produção, o próximo passo seria Alembic.

## Mapa de UPAs próximas

Aba "UPAs próximas": o cidadão informa só o CEP e vê as UPAs mais próximas em lista e em mapa Plotly (OpenStreetMap, com hover e zoom).

Fontes de dados abertos cruzadas com a entrada do cidadão:

- **ViaCEP:** CEP para endereço e código IBGE do município.
- **Nominatim (OpenStreetMap):** endereço para latitude e longitude.
- **AwesomeAPI:** coordenadas do CEP de cada unidade, usadas para conferir o cadastro do CNES.
- **CNES (DataSUS):** UPAs e pronto atendimentos do município, com coordenadas, telefone e turno. O backend pagina a API (20 por página), ignora cadastros sem coordenada ou desabilitados, guarda o resultado por 6 horas e calcula a distância (fórmula de haversine).

Privacidade: só o CEP é enviado, ele não é gravado e o cache do front guarda a consulta por 10 minutos. Qualidade da posição: as coordenadas do CNES às vezes erram. O backend cruza cada unidade com a posição do CEP dela (AwesomeAPI); se divergirem mais de 1,5 km, tenta corrigir pelo nome no OpenStreetMap (Nominatim) e reordena a lista. Se não conseguir corrigir, a unidade aparece marcada como "posição aproximada" no mapa e na lista. O botão "Como chegar" usa nome e endereço escritos, não coordenadas.

Limites conhecidos: o CNES pode ter telefone e horário desatualizados, e a busca cobre apenas o município do CEP.

## Fluxo CitizenTech

1. **Entrada:** formulário com validação (texto de 10 a 800 caracteres, faixa de idade, duração, sinais de alerta, confirmação de ciência).
2. **Processamento inteligente:** o front chama a API FastAPI, que chama o Gemini com saída estruturada (JSON Schema + modelo Pydantic). O front nunca fala com o provedor de IA.
3. **Resposta:** badge de urgência (cor + ícone + texto), serviço recomendado, ações práticas, sinais de alerta e protocolo.
4. **Human-in-the-loop:** o cidadão confirma ou corrige a urgência e avalia se foi útil. Só então a solicitação é considerada revisada.

Trava de segurança no pipeline: qualquer sinal de alerta grave marcado (dor no peito, falta de ar, desmaio, sangramento, confusão, sinais de AVC) eleva o resultado para emergência com SAMU, mesmo que a IA diga o contrário.

## Arquitetura

```mermaid
flowchart LR
    Cidadao --> Front["Streamlit (frontend)"]
    Front -->|HTTP JSON| Routers["FastAPI routers"]
    Routers --> Pipelines
    Pipelines --> Providers
    Providers -->|HTTPS| Gemini
    Routers --> Schemas
```

```
backend/
  app/
    routers/     um arquivo por serviço (health, meta, triage, review, units)
    schemas/     modelos Pydantic de entrada e saída
    pipelines/   lógica de triagem, trava de segurança, revisão
    providers/   acesso ao Gemini e armazenamento em memória
  tests/         pytest, sem subir interface nem chamar a IA
frontend/
  features/      telas por responsabilidade
  ui/            tema e componentes reutilizáveis
  state/         estado da sessão e dados derivados
  providers/     cliente HTTP da API
```

## Como rodar

Copie `.env.example` para `.env` na raiz e preencha `GEMINIAPIKEY`, `SEGREDOAPP` (gere com `openssl rand -base64 48`) e as variáveis de e-mail. No Docker, preencha também `DBPASSWORD`.

### Local

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:aplicacao --port 8000
```

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Docker

```bash
docker compose up --build
```

Front em `http://localhost:8501`, API em `http://localhost:8000/docs`.

### Testes

```bash
cd backend
pytest
```

## Deploy

Arquitetura publicada: front no Streamlit Community Cloud, API no Render (Docker) e banco PostgreSQL no Neon. O Docker Compose sobe tudo junto (Opção B) e a hospedagem em plataformas é a Opção A.

PREENCHER depois de publicar: link do front e link da API (`/docs`).

### 1. Banco (Neon)
1. Crie um projeto no Neon e copie a connection string (`postgresql://...?sslmode=require`).
2. Ela vai em `DATABASEURL` na API. As tabelas são criadas na primeira conexão.

### 2. API (Render)
1. No Render, crie um *Blueprint* a partir deste repositório (usa o `render.yaml`) ou um *Web Service* com Docker, plano Free, *Root Directory* vazio e *Dockerfile Path* `./backend/Dockerfile`.
2. Preencha as variáveis marcadas como secretas: `GEMINIAPIKEY`, `DATABASEURL`, `BREVOAPIKEY`, `SENDEREMAIL` e `ALLOWEDORIGINS` (a URL do front).
3. `SEGREDOAPP` é gerado pelo próprio Render. `MOSTRARCODIGONOLOG` deve ficar `false`.
4. Confira `https://SUA-API.onrender.com/health`.

O plano gratuito do Render desliga a API após 15 minutos sem uso e a primeira chamada seguinte leva de 30 a 60 segundos. Por isso o front usa timeout de 90 segundos.

### 3. Front (Streamlit Community Cloud)
1. Em share.streamlit.io, crie um app com o repositório, a branch `main` e o arquivo principal `frontend/app.py`.
2. Em *Advanced settings*, escolha Python 3.12 e cole em *Secrets* o conteúdo de `frontend/.streamlit/secrets.toml.example`, trocando `APIURL` pela URL real da API.

### Docker (Opção B)
`docker compose up --build` sobe banco, API e front. Preencha `DBPASSWORD` no `.env`.

## Acessibilidade aplicada

- Urgência sempre comunicada por cor, ícone e texto.
- Contraste alto entre texto e fundo nos badges, cartões e gráficos.
- Todos os campos com rótulo claro e textos de ajuda.
- Foco de teclado visível em botões, campos e abas.
- Linguagem simples, sem termos técnicos.
- Mensagens de erro em português, sem detalhes técnicos.
- Gráficos com cores e rótulos textuais nos eixos.

## ODS

- **ODS 3 – Saúde e Bem-Estar:** PREENCHER justificativa.
- **ODS 10 – Redução das Desigualdades:** PREENCHER justificativa.

## Decisões técnicas

- **Streamlit:** abas, colunas e sidebar nativos, Plotly integrado, `session_state` e cache.
- **Gemini com JSON Schema:** garante campos previsíveis; a resposta ainda é revalidada com Pydantic.
- **Prompt:** proíbe diagnóstico e receitas, trata o relato como dado e, na dúvida, escolhe a urgência maior.
- **Estado e cache:** `session_state` guarda histórico e resultado atual (sem repetir chamada ao LLM a cada rerun); `cache_data` guarda as opções do formulário; `cache_resource` guarda o cliente HTTP.
- **Segredos:** chave só em variável de ambiente; `.env` fora do Git.
- **Privacidade:** o formulário não pede nome, CPF nem endereço.

## Ética e limites da IA

- Riscos: erro de classificação, viés, alucinação, uso como substituto de consulta.
- Não faz diagnóstico, não indica remédios, não substitui profissional de saúde.
- Mitigações: trava de sinais graves, aviso fixo, revisão humana obrigatória antes de considerar a solicitação concluída.
- PREENCHER: demais limites observados nos testes.

## Evidências de validação

### Teste com pessoas do público-alvo

PREENCHER: mínimo de 3 pessoas, roteiro curto, observações e um ajuste feito a partir do feedback.

| Pessoa | Perfil | Tarefa | Observação | Ajuste feito |
|---|---|---|---|---|
| | | | | |

### Casos de teste da IA

PREENCHER com resultados reais obtidos (mínimo de 3 casos).

| Entrada | Saída esperada | Saída obtida | Ajuste realizado |
|---|---|---|---|
| | | | |
