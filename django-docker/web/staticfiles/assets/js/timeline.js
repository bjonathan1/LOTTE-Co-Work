/**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 *  
 * For more information visit:
 * https://www.amcharts.com/
 * 
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */

// Themes begin
// Themes end

var chart = am4core.create("chartdiv", am4charts.XYChart);
chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

chart.paddingRight = 30;
chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm";

var colorSet = new am4core.ColorSet();
colorSet.saturation = 0.4;

chart.data = [ {
  "category": "앱 2.0 프로젝트",
  "start": "2019-07-02",
  "end": "2019-07-14",
  "color": colorSet.getIndex(0).brighten(0),
  "task": "앱 UI/UX 기획"
}, {
  "category": "앱 2.0 프로젝트",
  "start": "2019-07-15",
  "end": "2019-07-30",
  "color": colorSet.getIndex(0).brighten(0.4),
  "task": "앱 UI/UX 디자인"
}, {
  "category": "앱 2.0 프로젝트",
  "start": "2019-08-01",
  "end": "2019-08-03",
  "color": colorSet.getIndex(0).brighten(0.8),
  "task": "사용성 검토"
}, {
  "category": "앱 2.0 프로젝트",
  "start": "2019-08-18",
  "end": "2019-08-30",
  "color": colorSet.getIndex(0).brighten(1.2),
  "task": "앱 개발팀 미팅 및 작업 발주"
}, {
  "category": "CRM 프로젝트",
  "start": "2019-05-20",
  "end": "2019-05-25",
  "color": colorSet.getIndex(2).brighten(0),
  "task": "CRM 현황 파악"
}, {
  "category": "CRM 프로젝트",
  "start": "2019-06-01",
  "end": "2019-06-24",
  "color": colorSet.getIndex(2).brighten(0.4),
  "task": "CRM 개선점 도출 및 시뮬레이션"
}, {
  "category": "CRM 프로젝트",
  "start": "2019-06-24",
  "end": "2019-07-07",
  "color": colorSet.getIndex(2).brighten(0.8),
  "task": "사용성 검토"
}, {
  "category": "CRM 프로젝트",
  "start": "2019-07-11",
  "end": "2019-09-09",
  "color": colorSet.getIndex(2).brighten(1.2),
  "task": "New CRM 시스템 개발"
}, {
  "category": "개인화 프로젝트",
  "start": "2019-07-10",
  "end": "2019-07-15",
  "color": colorSet.getIndex(4).brighten(0),
  "task": "유통업 개인화 사례 조사"
}, {
  "category": "개인화 프로젝트",
  "start": "2019-07-20",
  "end": "2019-08-01",
  "color": colorSet.getIndex(4).brighten(0.4),
  "task": "필요 데이터 확보 계획 및 전략 수립"
}, {
  "category": "개인화 프로젝트",
  "start": "2019-08-01",
  "end": "2019-08-30",
  "color": colorSet.getIndex(4).brighten(0.8),
  "task": "필요데이터 확보"
}, {
  "category": "개인화 프로젝트",
  "start": "2019-09-02",
  "end": "2019-11-05",
  "color": colorSet.getIndex(4).brighten(1.2),
  "task": "개인화 알고리즘 개발 및 적용"
}, {
  "category": "VOC 프로젝트",
  "start": "2019-07-14",
  "end": "2019-07-20",
  "color": colorSet.getIndex(6).brighten(0),
  "task": "현 VOC 시스템 현황 파악"
}, {
  "category": "VOC 프로젝트",
  "start": "2019-07-20",
  "end": "2019-07-27",
  "color": colorSet.getIndex(6).brighten(0.4),
  "task": "VOC 시스템 개선점 도출"
}, {
  "category": "VOC 프로젝트",
  "start": "2019-07-27",
  "end": "2019-08-11",
  "color": colorSet.getIndex(6).brighten(0.8),
  "task": "New VOC 시스템 개발"
}, {
  "category": "상품추천 프로젝트",
  "start": "2019-05-22",
  "end": "2019-05-29",
  "color": colorSet.getIndex(8).brighten(0),
  "task": "유통업 상품추천 사례 조사"
}, {
  "category": "상품추천 프로젝트",
  "start": "2019-06-01",
  "end": "2019-06-29",
  "color": colorSet.getIndex(8).brighten(0.4),
  "task": "필요데이터 확보 계획 및 전략 수립"
}, {
  "category": "상품추천 프로젝트",
  "start": "2019-06-30",
  "end": "2019-08-02",
  "color": colorSet.getIndex(8).brighten(0.8),
  "task": "필요데이터 확보"
}, {
  "category": "상품추천 프로젝트",
  "start": "2019-08-13",
  "end": "2019-11-17",
  "color": colorSet.getIndex(8).brighten(1.2),
  "task": "상품추천 알고리즘 개발 및 적용"
} ];

chart.dateFormatter.dateFormat = "yyyy-MM-dd";
chart.dateFormatter.inputDateFormat = "yyyy-MM-dd";

var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "category";
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.renderer.inversed = true;

var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
dateAxis.renderer.minGridDistance = 70;
dateAxis.baseInterval = { count: 1, timeUnit: "day" };
// dateAxis.max = new Date(2018, 0, 1, 24, 0, 0, 0).getTime();
//dateAxis.strictMinMax = true;
dateAxis.renderer.tooltipLocation = 0;

var series1 = chart.series.push(new am4charts.ColumnSeries());
series1.columns.template.height = am4core.percent(70);
series1.columns.template.tooltipText = "{task}: [bold]{openDateX}[/] - [bold]{dateX}[/]";

series1.dataFields.openDateX = "start";
series1.dataFields.dateX = "end";
series1.dataFields.categoryY = "category";
series1.columns.template.propertyFields.fill = "color"; // get color from data
series1.columns.template.propertyFields.stroke = "color";
series1.columns.template.strokeOpacity = 1;

chart.scrollbarX = new am4core.Scrollbar();
