RESUMO DO **ARTIGO 1**

**Radiogenómica e radiomics**: A radiogenómica combina dados radiológicos (radiomics) com informações genéticas. Radiomics refere-se à extração de dados quantitativos de imagens médicas, como tomografias (CT) e ressonâncias magnéticas (MRI), que podem revelar padrões ocultos não visíveis a olho nu. Estes dados podem ser correlacionados com perfis genéticos para prever mutações específicas e ajudar na seleção de tratamentos.

**Implicações no cancro do pulmão**: A integração de radiogenómica pode prever mutações importantes, como as do gene EGFR, ALK, e KRAS, que são cruciais para determinar terapias específicas em doentes com cancro do pulmão de células não pequenas (NSCLC). Estudos têm mostrado que modelos baseados em radiomics podem alcançar uma elevada precisão na previsão destas mutações quando combinados com variáveis clínicas.

**Vantagens da radiogenómica**: A radiogenómica pode ser usada para identificar mutações e prever a resposta ao tratamento de forma não invasiva, minimizando a necessidade de biópsias, que podem ser complicadas e nem sempre refletem toda a heterogeneidade tumoral. Além disso, pode prever respostas à imunoterapia e a terapias-alvo.

**Desafios atuais**: Apesar do potencial, a aplicação clínica da radiogenómica ainda enfrenta desafios, como a necessidade de padronização dos modelos e a necessidade de grandes conjuntos de dados para treinar modelos robustos. A falta de uniformidade nos protocolos de aquisição de imagens e nos métodos de análise também limita a replicabilidade dos resultados entre diferentes centros.

**Perspectivas futuras**: O artigo destaca que, embora a radiogenómica se mostre muito promissora, mais estudos são necessários para padronizar e validar os modelos. A combinação de dados de múltiplas fontes, incluindo dados clínicos e histopatológicos, será crucial para melhorar a precisão das previsões e integrar essa abordagem na prática clínica diária.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

RESUMO DO **ARTIGO 2**

Radiomics é a análise quantitativa de características extraídas de imagens médicas (como CT e PET), com o objetivo de captar informações biológicas e prognósticas que não são visíveis ao olho nu. Estas características, conhecidas como features, podem ser usadas para diagnóstico, estratificação do prognóstico e avaliação da resposta ao tratamento.

**Avaliação de Nódulos Pulmonares**: A radiomics ajuda na caracterização de nódulos pulmonares, distinguindo entre nódulos benignos e malignos. As assinaturas radiómicas são especialmente úteis na diferenciação de adenocarcinomas e granulomas.

**Estratificação Prognóstica e Avaliação da Resposta ao Tratamento**: Características extraídas de imagens podem prever a agressividade do tumor e a resposta ao tratamento. Tumores com maior heterogeneidade textural têm sido associados a piores prognósticos.

**Previsão de Metástases em Linfonodos**: Radiomics também foi aplicada para prever metástases em linfonodos mediastinais, com modelos baseados em características radiómicas que alcançaram boa precisão na previsão de metástases em pacientes com cancro do pulmão.

**Radiogenómica (Imaging Genomics)**: A radiogenómica usa radiomics para identificar perfis genéticos, como mutações nos genes EGFR, ALK e KRAS, permitindo uma abordagem mais personalizada no tratamento.

**Desafios Técnicos**:
- A segmentação precisa do tumor, ou seja, a separação do tumor das estruturas circundantes, é crítica para garantir a precisão das características extraídas. Métodos automáticos e semiautomáticos estão a ser desenvolvidos para melhorar essa etapa.
- A qualidade e os parâmetros das imagens podem influenciar as características extraídas. Estudos indicam que a espessura das fatias de tomografia (slices) afeta significativamente os resultados. Imagens mais finas (ex: 1,25 mm) oferecem uma melhor precisão na extração de características.

**Perspectivas futuras**: Embora radiomics mostre grande promessa, ainda existem desafios para a sua aplicação clínica de rotina, como a padronização e validação dos modelos. O desenvolvimento de software open-source e a colaboração entre instituições são cruciais para o avanço deste campo.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

RESUMO DO **ARTIGO 3**

O estudo investiga a eficácia de características texturais profundas extraídas de imagens de textura em comparação com as características de intensidade tradicionais para melhorar a predição de malignidade.

**Objetivo do Estudo**: Avaliar se as características texturais profundas (extraídas com GLCM - Gray-Level Co-occurrence Matrix) têm um impacto positivo na previção de malignidade de nódulos pulmonares, comparando-as com características de intensidade extraídas diretamente das imagens de tomografia computorizada (CT).

**Estratégia de Fusão de Características**: Foram exploradas três estratégias para a fusão de características extraídas de várias imagens de textura: concatenação, média e utilização sem fusão. As características foram extraídas através da rede VGG16 pré-treinada, e as previsões de malignidade foram feitas com um classificador SVM.As imagens de textura foram processadas usando características GLCM para descrever padrões de textura a partir da região de interesse (ROI) do nódulo.

**Divisão de Dados e Validação**: O estudo utilizou diferentes níveis de generalização para avaliar o desempenho dos modelos. Foram adotadas técnicas como k-fold cross-validation, divisão por nódulo e divisão por fatias de imagens. A técnica de "leave-one-nodule-out" também foi aplicada para avaliar a capacidade de generalização do modelo em novos dados.

**Resultados**:
- As características de intensidade apresentaram o pior desempenho. As características texturais extraídas com GLCM superaram as características de intensidade, especialmente quando combinadas pela estratégia de concatenação.
- A fusão de características via concatenação resultou em uma sensibilidade de 1.0 e especificidade de 0.99 no diagnóstico de nódulos malignos, quando divididos por fatias. No entanto, o desempenho foi mais realista, mas menos otimista, ao dividir os dados por nódulos inteiros.
- A variabilidade nos resultados destaca os desafios em obter previsões consistentes e confiáveis devido ao tamanho limitado do conjunto de dados e à necessidade de mais amostras benignas para melhorar a precisão.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

