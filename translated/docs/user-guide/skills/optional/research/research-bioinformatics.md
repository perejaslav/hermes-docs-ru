На этой странице
Шлюз к 400+ биоинформатическим навыкам из bioSkills и ClawBio. Охватывает геномику, транскриптомику, одноклеточный анализ, поиск вариантов, фармакогеномику, метагеномику, структурную биологию и многое другое. Запрашивает профильные справочные материалы по требованию.
## Метаданные навыка[​](<#skill-metadata> "Прямая ссылка на Метаданные навыка")
|   | 
|---|---  
|Источник| Опционально — установка: `hermes skills install official/research/bioinformatics`  
|Путь| `optional-skills/research/bioinformatics`  
|Версия| `1.0.0`  
|Платформы| linux, macos  
|Теги| `bioinformatics`, `genomics`, `sequencing`, `biology`, `research`, `science`  
## Справочно: полный SKILL.md[​](<#reference-full-skillmd> "Прямая ссылка на Справочно: полный SKILL.md")
info
Ниже приведено полное описание навыка, которое Hermes загружает при его активации. Это инструкции, которые видит агент, когда навык активен.
# Шлюз биоинформатических навыков
Используйте, когда запрос касается биоинформатики, геномики, секвенирования, поиска вариантов, экспрессии генов, одноклеточного анализа, структуры белков, фармакогеномики, метагеномики, филогенетики или любой вычислительной биологии.
Этот навык является шлюзом к двум библиотекам биоинформатических навыков с открытым исходным кодом. Вместо того чтобы включать сотни профильных навыков, он индексирует их и загружает необходимое по требованию.
## Источники[​](<#sources> "Прямая ссылка на Источники")
◆ **bioSkills** — 385 справочных навыков (шаблоны кода, руководства по параметрам, деревья решений) Репозиторий: <https://github.com/GPTomics/bioSkills> Формат: SKILL.md по каждой теме с примерами кода. Python/R/CLI.
◆ **ClawBio** — 33 запускаемых пайплайна (исполняемые скрипты, пакеты воспроизводимости) Репозиторий: <https://github.com/ClawBio/ClawBio> Формат: Python-скрипты с демонстрациями. Каждый анализ экспортирует report.md + commands.sh + environment.yml.
## Как загрузить и использовать навык[​](<#how-to-fetch-and-use-a-skill> "Прямая ссылка на Как загрузить и использовать навык")
  1. Определите домен и название навыка из указателя ниже.
  2. Клонируйте соответствующий репозиторий (поверхностное клонирование для экономии времени):
[code] # bioSkills (справочные материалы)  
        git clone --depth 1 https://github.com/GPTomics/bioSkills.git /tmp/bioSkills  
          
        # ClawBio (запускаемые пайплайны)  
        git clone --depth 1 https://github.com/ClawBio/ClawBio.git /tmp/ClawBio  
        
[/code]
  3. Прочитайте конкретный навык:
[code] # bioSkills — каждый навык находится по пути: <category>/<skill-name>/SKILL.md  
        cat /tmp/bioSkills/variant-calling/gatk-variant-calling/SKILL.md  
          
        # ClawBio — каждый навык находится по пути: skills/<skill-name>/  
        cat /tmp/ClawBio/skills/pharmgx-reporter/README.md  
        
[/code]
  4. Используйте загруженный навык как справочный материал. Эти навыки НЕ в формате SKILL.md для Hermes — у них своя структура. Воспринимайте их как экспертные руководства по домену. Они содержат правильные параметры, корректные флаги инструментов и проверенные пайплайны.


## Указатель навыков по доменам[​](<#skill-index-by-domain> "Прямая ссылка на Указатель навыков по доменам")
### Основы работы с последовательностями[​](<#sequence-fundamentals> "Прямая ссылка на Основы работы с последовательностями")
bioSkills: sequence-io/ — read-sequences, write-sequences, format-conversion, batch-processing, compressed-files, fastq-quality, filter-sequences, paired-end-fastq, sequence-statistics sequence-manipulation/ — seq-objects, reverse-complement, transcription-translation, motif-search, codon-usage, sequence-properties, sequence-slicing ClawBio: seq-wrangler — Контроль качества последовательностей, выравнивание и обработка BAM (обёртка FastQC, BWA, SAMtools)
### Контроль качества чтений и выравнивание[​](<#read-qc--alignment> "Прямая ссылка на Контроль качества чтений и выравнивание")
bioSkills: read-qc/ — quality-reports, fastp-workflow, adapter-trimming, quality-filtering, umi-processing, contamination-screening, rnaseq-qc read-alignment/ — bwa-alignment, star-alignment, hisat2-alignment, bowtie2-alignment alignment-files/ — sam-bam-basics, alignment-sorting, alignment-filtering, bam-statistics, duplicate-handling, pileup-generation
### Поиск вариантов и аннотация[​](<#variant-calling--annotation> "Прямая ссылка на Поиск вариантов и аннотация")
bioSkills: variant-calling/ — gatk-variant-calling, deepvariant, variant-calling (bcftools), joint-calling, structural-variant-calling, filtering-best-practices, variant-annotation, variant-normalization, vcf-basics, vcf-manipulation, vcf-statistics, consensus-sequences, clinical-interpretation ClawBio: vcf-annotator — Аннотация VEP + ClinVar + gnomAD с учётом популяционного контекста variant-annotation — Пайплайн аннотации вариантов
### Дифференциальная экспрессия (Bulk RNA-seq)[​](<#differential-expression-bulk-rna-seq> "Прямая ссылка на Дифференциальная экспрессия (Bulk RNA-seq)")
bioSkills: differential-expression/ — deseq2-basics, edger-basics, batch-correction, de-results, de-visualization, timeseries-de rna-quantification/ — alignment-free-quant (Salmon/kallisto), featurecounts-counting, tximport-workflow, count-matrix-qc expression-matrix/ — counts-ingest, gene-id-mapping, metadata-joins, sparse-handling ClawBio: rnaseq-de — Полный пайплайн DE с контролем качества, нормализацией и визуализацией diff-visualizer — Расширенная визуализация и отчётность для результатов DE
### Одноклеточный RNA-seq[​](<#single-cell-rna-seq> "Прямая ссылка на Одноклеточный RNA-seq")
bioSkills: single-cell/ — preprocessing, clustering, batch-integration, cell-annotation, cell-communication, doublet-detection, markers-annotation, trajectory-inference, multimodal-integration, perturb-seq, scatac-analysis, lineage-tracing, metabolite-communication, data-io ClawBio: scrna-orchestrator — Полный пайплайн Scanpy (QC, кластеризация, маркеры, аннотация) scrna-embedding — Латентное представление и интеграция партий на основе scVI
### Пространственная транскриптомика[​](<#spatial-transcriptomics> "Прямая ссылка на Пространственная транскриптомика")
bioSkills: spatial-transcriptomics/ — spatial-data-io, spatial-preprocessing, spatial-domains, spatial-deconvolution, spatial-communication, spatial-neighbors, spatial-statistics, spatial-visualization, spatial-multiomics, spatial-proteomics, image-analysis
### Эпигеномика[​](<#epigenomics> "Прямая ссылка на Эпигеномика")
bioSkills: chip-seq/ — peak-calling, differential-binding, motif-analysis, peak-annotation, chipseq-qc, chipseq-visualization, super-enhancers atac-seq/ — atac-peak-calling, atac-qc, differential-accessibility, footprinting, motif-deviation, nucleosome-positioning methylation-analysis/ — bismark-alignment, methylation-calling, dmr-detection, methylkit-analysis hi-c-analysis/ — hic-data-io, tad-detection, loop-calling, compartment-analysis, contact-pairs, matrix-operations, hic-visualization, hic-differential ClawBio: methylation-clock — Оценка эпигенетического возраста
### Фармакогеномика и клинические данные[​](<#pharmacogenomics--clinical> "Прямая ссылка на Фармакогеномика и клинические данные")
bioSkills: clinical-databases/ — clinvar-lookup, gnomad-frequencies, dbsnp-queries, pharmacogenomics, polygenic-risk, hla-typing, variant-prioritization, somatic-signatures, tumor-mutational-burden, myvariant-queries ClawBio: pharmgx-reporter — Отчёт PGx из данных 23andMe/AncestryDNA (12 генов, 31 SNP, 51 препарат) drug-photo — Фото лекарства → персонализированная карточка дозировки PGx (через vision) clinpgx — API ClinPGx для данных ген-препарат и руководств CPIC gwas-lookup — Федеративный поиск вариантов по 9 геномным базам данных gwas-prs — Полигенные баллы риска из потребительских генетических данных nutrigx_advisor — Персонализированное питание из потребительских генетических данных
### Популяционная генетика и GWAS[​](<#population-genetics--gwas> "Прямая ссылка на Популяционная генетика и GWAS")
bioSkills: population-genetics/ — association-testing (PLINK GWAS), plink-basics, population-structure, linkage-disequilibrium, scikit-allel-analysis, selection-statistics causal-genomics/ — mendelian-randomization, fine-mapping, colocalization-analysis, mediation-analysis, pleiotropy-detection phasing-imputation/ — haplotype-phasing, genotype-imputation, imputation-qc, reference-panels ClawBio: claw-ancestry-pca — PCA происхождения по референсной панели SGDP
### Метагеномика и микробиом[​](<#metagenomics--microbiome> "Прямая ссылка на Метагеномика и микробиом")
bioSkills: metagenomics/ — kraken-classification, metaphlan-profiling, abundance-estimation, functional-profiling, amr-detection, strain-tracking, metagenome-visualization microbiome/ — amplicon-processing, diversity-analysis, differential-abundance, taxonomy-assignment, functional-prediction, qiime2-workflow ClawBio: claw-metagenomics — Профилирование дробовой метагеномики (таксономия, резистом, функциональные пути)
### Сборка и аннотация геномов[​](<#genome-assembly--annotation> "Прямая ссылка на Сборка и аннотация геномов")
bioSkills: genome-assembly/ — hifi-assembly, long-read-assembly, short-read-assembly, metagenome-assembly, assembly-polishing, assembly-qc, scaffolding, contamination-detection genome-annotation/ — eukaryotic-gene-prediction, prokaryotic-annotation, functional-annotation, ncrna-annotation, repeat-annotation, annotation-transfer long-read-sequencing/ — basecalling, long-read-alignment, long-read-qc, clair3-variants, structural-variants, medaka-polishing, nanopore-methylation, isoseq-analysis
### Структурная биология и хемоинформатика[​](<#structural-biology--chemoinformatics> "Прямая ссылка на Структурная биология и хемоинформатика")
bioSkills: structural-biology/ — alphafold-predictions, modern-structure-prediction, structure-io, structure-navigation, structure-modification, geometric-analysis chemoinformatics/ — molecular-io, molecular-descriptors, similarity-searching, substructure-search, virtual-screening, admet-prediction, reaction-enumeration ClawBio: struct-predictor — Локальное предсказание структур AlphaFold/Boltz/Chai с возможностью сравнения
### Протеомика[​](<#proteomics> "Прямая ссылка на Протеомика")
bioSkills: proteomics/ — data-import, peptide-identification, protein-inference, quantification, differential-abundance, dia-analysis, ptm-analysis, proteomics-qc, spectral-libraries ClawBio: proteomics-de — Дифференциальная экспрессия протеомов
### Анализ путей и генные сети[​](<#pathway-analysis--gene-networks> "Прямая ссылка на Анализ путей и генные сети")
bioSkills: pathway-analysis/ — go-enrichment, gsea, kegg-pathways, reactome-pathways, wikipathways, enrichment-visualization gene-regulatory-networks/ — scenic-regulons, coexpression-networks, differential-networks, multiomics-grn, perturbation-simulation
### Иммуноинформатика[​](<#immunoinformatics> "Прямая ссылка на Иммуноинформатика")
bioSkills: immunoinformatics/ — mhc-binding-prediction, epitope-prediction, neoantigen-prediction, immunogenicity-scoring, tcr-epitope-binding tcr-bcr-analysis/ — mixcr-analysis, scirpy-analysis, immcantation-analysis, repertoire-visualization, vdjtools-analysis
### CRISPR и геномная инженерия[​](<#crispr--genome-engineering> "Прямая ссылка на CRISPR и геномная инженерия")
bioSkills: crispr-screens/ — mageck-analysis, jacks-analysis, hit-calling, screen-qc, library-design, crispresso-editing, base-editing-analysis, batch-correction genome-engineering/ — grna-design, off-target-prediction, hdr-template-design, base-editing-design, prime-editing-design
### Управление рабочими процессами[​](<#workflow-management> "Прямая ссылка на Управление рабочими процессами")
bioSkills: workflow-management/ — snakemake-workflows, nextflow-pipelines, cwl-workflows, wdl-workflows ClawBio: repro-enforcer — Экспорт любого анализа как пакета воспроизводимости (Conda env + Singularity + контрольные суммы) galaxy-bridge — Доступ к 8000+ инструментам Galaxy через usegalaxy.org
### Специализированные домены[​](<#specialized-domains> "Прямая ссылка на Специализированные домены")
bioSkills: alternative-splicing/ — splicing-quantification, differential-splicing, isoform-switching, sashimi-plots, single-cell-splicing, splicing-qc ecological-genomics/ — edna-metabarcoding, landscape-genomics, conservation-genetics, biodiversity-metrics, community-ecology, species-delimitation epidemiological-genomics/ — pathogen-typing, variant-surveillance, phylodynamics, transmission-inference, amr-surveillance liquid-biopsy/ — cfdna-preprocessing, ctdna-mutation-detection, fragment-analysis, tumor-fraction-estimation, methylation-based-detection, longitudinal-monitoring epitranscriptomics/ — m6a-peak-calling, m6a-differential, m6anet-analysis, merip-preprocessing, modification-visualization metabolomics/ — xcms-preprocessing, metabolite-annotation, normalization-qc, statistical-analysis, pathway-mapping, lipidomics, targeted-analysis, msdial-preprocessing flow-cytometry/ — fcs-handling, gating-analysis, compensation-transformation, clustering-phenotyping, differential-analysis, cytometry-qc, doublet-detection, bead-normalization systems-biology/ — flux-balance-analysis, metabolic-reconstruction, gene-essentiality, context-specific-models, model-curation rna-structure/ — secondary-structure-prediction, ncrna-search, structure-probing
### Визуализация данных и отчётность[​](<#data-visualization--reporting> "Прямая ссылка на Визуализация данных и отчётность")
bioSkills: data-visualization/ — ggplot2-fundamentals, heatmaps-clustering, volcano-customization, circos-plots, genome-browser-tracks, interactive-visualization, multipanel-figures, network-visualization, upset-plots, color-palettes, specialized-omics-plots, genome-tracks reporting/ — rmarkdown-reports, quarto-reports, jupyter-reports, automated-qc-reports, figure-export ClawBio: profile-report — Отчётность по профилю анализа data-extractor — Извлечение числовых данных из изображений научных графиков (через vision) lit-synthesizer — Поиск в PubMed/bioRxiv, обобщение, графы цитирований pubmed-summariser — Поиск генов/заболеваний в PubMed со структурированным обзором
### Доступ к базам данных[​](<#database-access> "Прямая ссылка на Доступ к базам данных")
bioSkills: database-access/ — entrez-search, entrez-fetch, entrez-link, blast-searches, local-blast, sra-data, geo-data, uniprot-access, batch-downloads, interaction-databases, sequence-similarity ClawBio: ukb-navigator — Семантический поиск по 12 000+ полям UK Biobank clinical-trial-finder — Поиск клинических исследований
### Планирование экспериментов[​](<#experimental-design> "Прямая ссылка на Планирование экспериментов")
bioSkills: experimental-design/ — power-analysis, sample-size, batch-design, multiple-testing
### Машинное обучение для омиксных данных[​](<#machine-learning-for-omics> "Прямая ссылка на Машинное обучение для омиксных данных")
bioSkills: machine-learning/ — omics-classifiers, biomarker-discovery, survival-analysis, model-validation, prediction-explanation, atlas-mapping ClawBio: claw-semantic-sim — Индекс семантического сходства для литературы по заболеваниям (PubMedBERT) omics-target-evidence-mapper — Агрегация свидетельств на уровне мишеней из омиксных источников
## Настройка окружения[​](<#environment-setup> "Прямая ссылка на Настройка окружения")
Эти навыки предполагают наличие биоинформатической рабочей станции. Типичные зависимости:
[code] 
    # Python  
    pip install biopython pysam cyvcf2 pybedtools pyBigWig scikit-allel anndata scanpy mygene  
      
    # R/Bioconductor  
    Rscript -e 'BiocManager::install(c("DESeq2","edgeR","Seurat","clusterProfiler","methylKit"))'  
      
    # CLI инструменты (Ubuntu/Debian)  
    sudo apt install samtools bcftools ncbi-blast+ minimap2 bedtools  
      
    # CLI инструменты (macOS)  
    brew install samtools bcftools blast minimap2 bedtools  
      
    # Или через Conda (рекомендуется для воспроизводимости)  
    conda install -c bioconda samtools bcftools blast minimap2 bedtools fastp kraken2  
    
[/code]
## Возможные проблемы[​](<#pitfalls> "Прямая ссылка на Возможные проблемы")
  * Загруженные навыки НЕ в формате SKILL.md Hermes. Они используют собственную структуру (bioSkills: сборники шаблонов кода; ClawBio: README + Python-скрипты). Читайте их как экспертные справочные материалы.
  * bioSkills — это справочные руководства: они показывают правильные параметры и шаблоны кода, но не являются исполняемыми пайплайнами.
  * Навыки ClawBio являются исполняемыми — у многих есть флаги `--demo`, и их можно запускать напрямую.
  * Оба репозитория предполагают, что биоинформатические инструменты уже установлены. Перед запуском пайплайнов проверяйте prerequisites.
  * Для ClawBio сначала выполните `pip install -r requirements.txt` в клонированном репозитории.
  * Файлы геномных данных могут быть очень большими. Следите за дисковым пространством при загрузке референсных геномов, наборов данных SRA или построении индексов.


  * [Метаданные навыка](<#skill-metadata>)
  * [Справочно: полный SKILL.md](<#reference-full-skillmd>)
  * [Источники](<#sources>)
  * [Как загрузить и использовать навык](<#how-to-fetch-and-use-a-skill>)
  * [Указатель навыков по доменам](<#skill-index-by-domain>)
    * [Основы работы с последовательностями](<#sequence-fundamentals>)
    * [Контроль качества чтений и выравнивание](<#read-qc--alignment>)
    * [Поиск вариантов и аннотация](<#variant-calling--annotation>)
    * [Дифференциальная экспрессия (Bulk RNA-seq)](<#differential-expression-bulk-rna-seq>)
    * [Одноклеточный RNA-seq](<#single-cell-rna-seq>)
    * [Пространственная транскриптомика](<#spatial-transcriptomics>)
    * [Эпигеномика](<#epigenomics>)
    * [Фармакогеномика и клинические данные](<#pharmacogenomics--clinical>)
    * [Популяционная генетика и GWAS](<#population-genetics--gwas>)
    * [Метагеномика и микробиом](<#metagenomics--microbiome>)
    * [Сборка и аннотация геномов](<#genome-assembly--annotation>)
    * [Структурная биология и хемоинформатика](<#structural-biology--chemoinformatics>)
    * [Протеомика](<#proteomics>)
    * [Анализ путей и генные сети](<#pathway-analysis--gene-networks>)
    * [Иммуноинформатика](<#immunoinformatics>)
    * [CRISPR и геномная инженерия](<#crispr--genome-engineering>)
    * [Управление рабочими процессами](<#workflow-management>)
    * [Специализированные домены](<#specialized-domains>)
    * [Визуализация данных и отчётность](<#data-visualization--reporting>)
    * [Доступ к базам данных](<#database-access>)
    * [Планирование экспериментов](<#experimental-design>)
    * [Машинное обучение для омиксных данных](<#machine-learning-for-omics>)
  * [Настройка окружения](<#environment-setup>)
  * [Возможные проблемы](<#pitfalls>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-bioinformatics -->
