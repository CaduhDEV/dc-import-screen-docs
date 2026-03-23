# Documentação de Importação de Leads

## Introdução

Esta documentação descreve o processo de importação de leads no sistema CRM, incluindo os campos de dados necessários, as etapas do processo e considerações importantes. O sistema suporta a importação de leads a partir de arquivos Excel (.xlsx) e CSV, permitindo a integração eficiente de dados de leads em massa.

### Campos de Dados do Lead

Todos os campos na planilha são tratados como texto, mas alguns requerem formatos específicos para validação correta:

| Campo | Tipo | Descrição | Formato Exemplo |
|-------|------|-----------|-----------------|
| Nome | Texto | Nome completo do lead | João Silva |
| Telefone | Texto | Número com DDI e DDD | +55 11 99999-9999 |
| Email | Texto | Endereço de email válido | joao@email.com |
| Documento | Texto | CPF, RG ou ID | 123.456.789-00 |
| Empresa | Texto | Nome da empresa | Empresa XYZ |
| Endereço | Texto | Rua/avenida | Rua das Flores |
| Número | Texto | Número do endereço | 123 |
| Bairro | Texto | Bairro | Centro |
| Cidade | Texto | Cidade | São Paulo |
| UF | Texto | Estado | SP |
| País | Texto | País | Brasil |
| Data de Nascimento | Data | Data no formato suportado | 15-05-1990 |
| Origem | Texto | Origem do lead | Facebook Ads |
| CEP | Texto | Código postal | 01234-567 |
| Complemento | Texto | Complemento do endereço | Apto 45 |
| Notas | Texto | Observações adicionais | Lead interessado em produto X |

**Observações importantes:**
- Formatos de data suportados: DD-MM-AAAA, DD-MM-AA, AAAA-MM-DD, AAAA-DD-MM, ISO, Timestamp
- Emails devem seguir o padrão `usuario@provedor.com`
- Telefones devem incluir DDI quando aplicável

## Processo de Importação

O processo de importação é dividido em 4 etapas principais, guiando o usuário através do upload, mapeamento e configuração dos dados.

### Etapa 1: Importação do Arquivo

**Formatos suportados:** XLSX, CSV  
**Peso máximo:** 4MB  
**Limitações:** Não é possível enviar múltiplos arquivos em um único processo.

#### O que deve conter na planilha?
- A planilha deve ser mapeada pelo usuário no sistema
- O sistema exibe as colunas disponíveis para mapeamento
- O usuário define qual coluna corresponde a cada campo do lead
- **Importante:** A definição correta dos campos é crucial para o sucesso da importação

#### Opção de Ignorar Cabeçalhos
- Toggle disponível para ignorar a primeira linha (cabeçalhos)
- Útil quando a planilha já possui nomes de colunas

#### Interface
- **Botão Voltar:** Cancela o upload
- **Botão Próximo:** Avança para a próxima etapa

### Etapa 2: Verificações

O sistema apresenta uma visualização da planilha importada, permitindo ao usuário mapear as colunas corretamente.

#### Funcionalidades
- Visualização UX da planilha
- Opção de ignorar cabeçalhos
- Mapeamento manual de colunas para campos do sistema

#### Formatos de Data Suportados
- DD-MM-AAAA
- DD-MM-AA
- AAAA-MM-DD
- AAAA-DD-MM
- ISO
- Timestamp

#### Interface
- **Botão Voltar:** Retorna à etapa anterior
- **Botão Próximo:** Avança para atribuições

### Etapa 3: Tela de Atribuições

Adicione informações padronizadas a todos os leads importados de uma só vez.

#### Campos Disponíveis

1. **Tags**
   - Defina tags para categorizar os leads
   - Atalho para criar novas tags

2. **Produtos**
   - Vincule produtos aos leads
   - Atalho para criar novos produtos

3. **Pipeline**
   - Inicie os leads em uma pipeline específica

4. **DDI de Telefones**
   - Padronize o DDI para todos os leads
   - **Atenção:** Use apenas se todos os leads forem do mesmo país

#### Interface
- **Botão Voltar:** Retorna à etapa anterior
- **Botão Próximo:** Avança para conclusão

### Etapa 4: Conclusão

Visualize uma prévia dos dados antes da importação final.

#### Funcionalidades
- Prévia de como os leads aparecerão na lista
- Alertas visuais para emails inválidos
- Processo de importação assíncrono

#### Processo de Importação
- Clique em "Completar Importação" para iniciar
- O tempo de processamento varia com o tamanho do arquivo
- Navegação normal permitida durante o processamento
- Notificações quando concluído

#### Estados Especiais
- Se o processo for interrompido, um botão "Pendente" aparece na página de leads

#### Interface
- **Botão Voltar:** Retorna à etapa anterior
- **Botão Excluir:** Cancela toda a operação

## Bugs Conhecidos

### Bug 1: Impossível Importar Leads de Países Distintos
**Descrição:** O sistema obriga a seleção de um único DDI na Etapa 3, impedindo a importação de leads com números de países diferentes.

**Impacto:** Números de telefone são truncados ou incorretamente formatados quando leads de múltiplos países são importados.

**Status:** Reportado - requer correção no sistema de DDI.

### Bug 2: Travamento ao Importar CSV
**Descrição:** O painel CRM trava completamente ao tentar importar arquivos CSV idênticos aos XLSX.

**Sintomas:** Sem erros nos logs, network ou console do navegador.

**Status:** Reportado - requer investigação do processamento de CSV.

## Gerador de Leads para Testes QA

Para facilitar os testes de capacidade de importação de dados pela equipe de QA, foi desenvolvido um script Python (`gerador_leads.py`) que gera leads fictícios em massa.

### Funcionalidades
- Gera leads para todos os países com DDIs correspondentes
- Cria dados aleatórios realistas para todos os campos
- Exporta para ambos os formatos suportados: XLSX e CSV
- Inclui validação de formatos de data e email

### Como Usar
1. Execute o script: `python gerador_leads.py`
2. Arquivos gerados:
   - `leads_completos_xlsx.xlsx`
   - `leads_completos_csv.csv`

### Benefícios para QA
- Teste de importação com dados diversos
- Validação de mapeamento de colunas
- Teste de performance com grandes volumes
- Verificação de tratamento de DDIs internacionais

Este gerador permite testar cenários complexos de importação, incluindo leads de múltiplos países, ajudando a identificar e corrigir bugs antes do lançamento.