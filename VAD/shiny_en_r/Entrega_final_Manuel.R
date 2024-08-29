if (!require(pacman)) {
  install.packages("pacman")
  library(pacman)
}
pacman::p_load(shinythemes, shiny, ggplot2, plotly, ggplot2, lubridate)

ui<-navbarPage(theme = shinytheme("sandstone"),
               "App Master Ciencia de datos",
               tabsetPanel( 
                 tabPanel("Selección de máquina", 
                          sidebarLayout(
                            sidebarPanel(
                              h5("MÁQUINA"),
                              fileInput("DatosFichero", "Selecciona un fichero", accept = NULL),
                              uiOutput("Selectmaquina")   
                            ),
                            mainPanel(h4("Probabilidad de orden"),
                                      br(),
                                      plotOutput("Prob_orden")
                            ))),
                 navbarMenu("Estado de la máquina",
                            tabPanel("Evolución temporal alarmas",
                                     sidebarPanel(
                                       p("Alarmas RadioButtons"),
                                       uiOutput("alarmas_radiobuttons")
                                     ),
                                     mainPanel(h4("Evolución temporal Alarmas"),
                                               br(),
                                               plotOutput("Evolucion_alarmas")
                                     )
                            ), 
                            tabPanel("Registros de la máquina",
                                     fluidRow(
                                       
                                       sidebarPanel(
                                         p("Alarmas checkbox"),
                                         uiOutput("alarmas_checkbox"),
                                         checkboxGroupInput("CheckBoxAlarm", "")
                                       ),
                                       mainPanel(h4("Registros de la máquina seleccionada"),
                                                 br(),
                                                 dataTableOutput('tabla'))
                                       
                                     )
                            )
                 ),
                 tabPanel("Estadísticas Globales Temporales", 
                          sidebarLayout(
                            sidebarPanel(
                              h5("PERIODO Y ESTADÍSTICAS
 ", 
                              ),dateRangeInput('rango_fechas', label='Selecciona el periodo', start ='2016-01-01', end = '2016-12-31', format = "yyyy-mm-dd", separator= "a", language='es', weekstart=1),
                              
                              uiOutput("Select_alarma"),
                              sliderInput("slider1", label = "Ancho del bin del histograma", 
                                          min= 1, max = 50, value = 20, step= 1),
                              h5("BOXPLOT"),
                              checkboxInput("boton_alarmas","Todas las máquinas")
                              
                            ),
                            mainPanel(h4("Histograma de la alarma seleccionada"),
                                      br(),
                                      plotOutput("Histograma"),
                                      h4("Boxplot de la alarma seleccionada"),
                                      br(),
                                      plotOutput("Boxplot"))
                          )))
)

server <- function(input, output) { 
  datos <- reactive({
    req(input$DatosFichero)
    name<- load(input$DatosFichero$datapath)
    data <- eval(parse(text = name))
    data <- na.omit(data)
    return(data)
  })
  
  output$Selectmaquina <- renderUI({
    selectInput("Selectmaquina", "Selecciona máquina", choices = unique(datos()$matricula))
  })
  
  output$alarmas_radiobuttons <- renderUI({
    radioButtons("alarmas_radiobuttons", "Selecciona la alarma a visualizar", colnames(datos())[5:length(colnames(datos()))-1])
  })
  
  output$alarmas_checkbox <- renderUI({
    checkboxGroupInput("alarmas_checkbox", "Selecciona las alarmas para ver en la tabla", colnames(datos())[5:length(colnames(datos()))-1],
                       selected = colnames(datos())[4])
  })
  
  output$Select_alarma <- renderUI({ 
    selectInput("Select_alarma","Alarma", colnames(datos())[5:length(colnames(datos()))-1]) 
  })
  
  output$Prob_orden <- renderPlot({
    ggplot(subset(datos(),matricula == input$Selectmaquina), aes(x = dia, y = p_orden,color=p_orden)) +
      geom_line() +
      geom_point() +scale_color_gradient(low = "blue", high = "red")+
      labs(x = "dia", y = "p_orden")
  })
  
  output$Evolucion_alarmas <- renderPlot({
    ggplot(subset(datos(),matricula == input$Selectmaquina), aes_string(x = 'dia', y = input$alarmas_radiobuttons)) +
      geom_line() +
      geom_point() +
      labs(x = "dia", y = input$alarmas_radiobuttons)
  })
  
  output$Boxplot <- renderPlot({
    if (!input$boton_alarmas) {
      data <- subset(datos(), matricula == input$Selectmaquina & dia <= input$rango_fechas[2] & dia >= input$rango_fechas[1])
      data_y <- data[[input$Select_alarma]]
      ggplot(data = data, aes(x = factor(matricula), y = data_y)) + 
        geom_boxplot() +
        labs(x = "matricula", y = input$Select_alarma)
    } else {
      data <- subset(datos(), dia <= input$rango_fechas[2] & dia >= input$rango_fechas[1])
      data_y <- data[[input$Select_alarma]]
      ggplot(data = data, aes(x = factor(matricula), y = data_y)) + 
        geom_boxplot() +
        labs(x = "matricula", y = input$Select_alarma)
    }
  })
  
  
  output$Histograma <- renderPlot({
    data <- subset(datos(), matricula == input$Selectmaquina & dia >= input$rango_fechas[1] & dia <= input$rango_fechas[2])
    ggplot(data = data, aes_string(x = input$Select_alarma)) +
      geom_histogram(binwidth = input$slider1) +
      labs(x = input$Select_alarma, y = 'count')
  })
  
  output$tabla <- renderDataTable(subset(datos(), matricula == input$Selectmaquina)[c("matricula","dia",input$alarmas_checkbox,"p_orden")])
  
}

shinyApp(ui, server)