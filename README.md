# Программа обработки экспериментальных данных

## Todo

- Загруженный файл может быть 200 МБ [максимально](https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader).
- Графопостроение с интерактивными элементами (как в qt-варианте бэкенда matplotlib).
- Неограниченное количество каналов для обработки.
- Возможность открытия файлов приборов, не реализованных на данный момент.
- Коэффициенты преобразования.
- Минимальные и максимальные значения ограничений по времени, окна скользящей средней и числа выборок для определения сдвига ноля.

## UML-диаграммы

### Диаграмма классов

```mermaid
classDiagram

class Opener {
	+cfg: dict ~dict~
	+read(file)
	+extract(file, device)
}

class Controller {
	+processor: Processor
	+last_file: str
	+run()
	+processing_start(cfg_in, file)
}


```

### Диаграмма последовательности

```mermaid
sequenceDiagram
    participant main
    participant controller
	participant configurator
	participant processor
	participant opener
	participant plotter
	actor ui

    activate main
    main ->>+ controller: create
    controller ->>+ configurator: create
    Note right of configurator: load from file<br>to default_cfg
    configurator ->> configurator: default_cfg to cfg
    controller ->>+ processor: create
    processor ->>+ opener: create
    processor ->>+ plotter: create
    main ->>+ ui: run via termilal as streamlit script

    ui ->> controller: processing_start
    controller ->> processor: file_processing(file)
    processor ->> opener: open(file)
    opener ->> opener: device detection
    opener ->> opener: load data from file
    opener -->> processor: return device and data
    processor ->> processor: self.raw_data to self.data
    processor ->> configurator: device_cfg_extract(action, device)
    processor ->> processor: processing
    processor ->> plotter: plotting
    ui ->> plotter: query to plot
    plotter -->> ui: plot draw

    loop when settings are changed, but file remains the same
    	ui ->> controller: cfg_update(key, value)
    	controller ->> configurator: cfg_update(key, value, device)
    	controller ->> processor: file_processing()
    	processor ->> processor: self.raw_data to self.data
    	processor ->> configurator: device_cfg_extract(action, device)
    	processor ->> processor: processing
    	processor ->> plotter: plotting
    	ui ->> plotter: query to plot
    	plotter -->> ui: plot draw
    end

    deactivate main
    deactivate controller
	deactivate configurator
	deactivate processor
	deactivate opener
	deactivate plotter
	deactivate ui
```