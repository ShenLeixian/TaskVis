<template>
  <div id="page">
    <div id="title-bar">
      <div id="title">TaskVis: Task-oriented Visualization Recommendation</div>
    </div>

    <div id="main-part">
      <div id="left-part">
        <!--   最左侧的窗口,用于选择Data和Setting   -->
        <el-card id="data-card"
                 class="card">
          <div slot="header"
               class="clearfix card-title">
            <img src="./assets/database.png" class="card-logo"/>
            <span>Data</span>
          </div>
          <el-select v-model="dataset_value"
                     placeholder="Choosing a Dataset"
                     @change="choose_dataset">
            <el-option v-for="item in dataset_options"
                       :key="item.value"
                       :label="item.label"
                       :value="item.value">
            </el-option>
          </el-select>
          <el-divider></el-divider>
          <div id="data-box">
            <div class="data-item"
                 :id="generate_id('data-item-', index)"
                 v-for="(item, index) in data_list"
                 v-bind:key="item.field"
                 @click="choose_data_item(item, index)">
              <div class="data-item-icon"
                   :id="generate_id('data-item-icon-' ,index)">{{data_type[item.type]}}</div>
              <div class="data-item-text">
                <div class="data-item-field"
                     :id="generate_id('data-item-field-', index)">{{item.field}}</div>
                <div class="data-item-type">{{item.type}}</div>
              </div>
            </div>
          </div>
        </el-card>

        <el-card id="setting-card"
                 class="card">
          <div slot="header"
               class="clearfix card-title">
            <img src="./assets/setting.png" class="card-logo"/>
            <span>Setting</span>
          </div>
          <div id="max-number-of-charts">
            <div class="setting-title">Max Number of Charts</div>
            <el-input-number id="max-number-of-charts-input"
                             v-model="max_number_of_charts"
                             size="mini"
                             :min="1"></el-input-number>
          </div>
          <el-divider></el-divider>
          <div id="recommendation-mode">
            <div class="setting-title">Recommendation Mode</div>
            <el-radio v-model="recommendation_mode_radio"
                      label="1">Individual Recommendation</el-radio>
            <el-radio v-model="recommendation_mode_radio"
                      label="2">Combination Recommendation</el-radio>
          </div>
          <el-divider></el-divider>
          <div id="ranking-scheme">
            <div class="setting-title">Ranking Scheme</div>
            <el-radio v-model="ranking_scheme_radio"
                      label="1" @change="ranking_change()">Complexity-based ranking</el-radio>
            <el-radio v-model="ranking_scheme_radio"
                      label="2" @change="ranking_change()">Reverse-complexity-based ranking</el-radio>
            <el-radio v-model="ranking_scheme_radio"
                      label="3" @change="ranking_change()">Interested-data-columns-based ranking</el-radio>
            <el-radio v-model="ranking_scheme_radio"
                      label="4" @change="ranking_change()">Tasks-coverage-based ranking</el-radio>
          </div>
        </el-card>
        <el-button id="recommendation-button"
                   type="primary"
                   @click="recommendation">Recommendation</el-button>
      </div>

      <div id="mid-part">
        <!--    中间的窗口，用于选择Task List    -->
        <el-card id="task-list-card"
                 class="card">
          <div slot="header"
               class="clearfix card-title">
            <img src="./assets/task.png" class="card-logo"/>
            <span>Task List</span>
          </div>
          <div id="task-box">
            <div class="task-item"
                 :id="generate_id('task-item-', index)"
                 v-for="(item, index) in task_list"
                 v-bind:key="item.task"
                 @click="choose_task_item(item, index)">
              <div class="task-item-name"
                   :id="generate_id('task-item-name-', index)">{{item.task}}</div>
              <div class="task-item-description"
                   :id="generate_id('task-item-description-', index)">{{item.description}}</div>
            </div>
          </div>
        </el-card>
      </div>

      <div id="right-part">
        <div id="right-setting-part">
          <div id="display-by-task-switch"><el-switch  :disabled="recommendation_mode !== '1'" v-model="display_by_task" active-text="Display by task" @change="display_by_task_change()"></el-switch></div>
          <div id="task_tag_box">
            <el-tag class="task-tag" v-for="item in chosen_task_items" v-bind:key="item">{{transform_from_task_name(item)}}</el-tag>
          </div>
        </div>
        <el-divider></el-divider>
        <div :key="1" v-if="!has_recommendation"></div>
        <div id="chart-part" :key="2" v-else>
          <div id="individual-recommendation-charts" v-if="recommendation_mode==='1'">
            <div id="individual-recommendation-display-by-task" v-if="display_by_task">
              <div class="vega-chart-area-by-task" v-for="(item, index) in chosen_task_items" v-if="recommendation_chart['Recos_nodedup'][item] !== undefined" v-bind:key="index">
                <div class="vega-chart-box-title" :id="generate_id('vega-chart-box-title-', item)"
                     @click="show_more_chart(item)">
                  {{transform_from_task_name(item)}}
                  <div class="triangle-left"></div>
                </div>
                <div class="vega-chart-box-by-task" :id="generate_id('vega-chart-box-by-', item)">
                  <div class="vega-chart" :id="generate_id('vega-chart-' + item + '-', chart_index)"
                       v-for="(chart_item, chart_index) in recommendation_chart['Recos_nodedup'][item]['R1']"
                       v-bind:key="chart_index" @click="show_chart_dialog(item, chart_index)"></div>
                </div>
              </div>
            </div>
            <div id="individual-recommendation-display-not-by-task" v-if="!display_by_task">
              <div class="vega-chart-box">
                <div class="vega-chart-with-task-title" v-for="(chart_item, chart_index) in recommendation_chart['Recos_dedup']['R1']" v-if="chart_index < max_number_of_charts_after_recommendation" v-bind:key="chart_index" >
                  <div class="vega-chart-task-title" v-if="ranking_scheme_radio==='1'"><el-tag class="vega-chart-task-title-tag" v-for="(tag_item, tag_index) in recommendation_chart['Recos_dedup']['R1'][chart_index]['task']" v-bind:key="tag_index" size="mini">{{tag_item}}</el-tag></div>
                  <div class="vega-chart-task-title" v-if="ranking_scheme_radio==='2'"><el-tag class="vega-chart-task-title-tag" v-for="(tag_item, tag_index) in recommendation_chart['Recos_dedup']['R2'][chart_index]['task']" v-bind:key="tag_index" size="mini">{{tag_item}}</el-tag></div>
                  <div class="vega-chart-task-title" v-if="ranking_scheme_radio==='3'"><el-tag class="vega-chart-task-title-tag" v-for="(tag_item, tag_index) in recommendation_chart['Recos_dedup']['R3'][chart_index]['task']" v-bind:key="tag_index" size="mini">{{tag_item}}</el-tag></div>
                  <div class="vega-chart-task-title" v-if="ranking_scheme_radio==='4'"><el-tag class="vega-chart-task-title-tag" v-for="(tag_item, tag_index) in recommendation_chart['Recos_dedup']['R4'][chart_index]['task']" v-bind:key="tag_index" size="mini">{{tag_item}}</el-tag></div>
                  <div class="vega-chart" :id="generate_id('vega-chart-', chart_index)"
                       @click="show_chart_dialog(null, chart_index)"></div>
                </div>
              </div>
            </div>
          </div>
          <div id="combination-recommendation-charts" v-if="recommendation_mode==='2'">
            <div class="vega-chart" :id="generate_id('vega-chart-', index)"
                 v-for="(item, index) in recommendation_chart" v-bind:key="index"
                 @click="show_chart_dialog(null, index)"></div>
            <div id="vega-chart-test"></div>
          </div>
        </div>
      </div>

      <el-dialog :visible.sync="chart_dialog_visible" width="1800px" center>
        <div id="dialog-chart"></div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
// import * as vega from 'vega'
import embed from 'vega-embed'

export default {
  name: 'App',
  data () {
    return {
      dataset_options: [{
        value: 'cars',
        label: 'Cars'
      }, {
        value: 'movies',
        label: 'Movie'
      }, {
        value: 'weather',
        label: 'Weather'
      }, {
        value: 'covid',
        label: 'Covid'
      }, {
        value: 'AirpotDeley',
        label: 'Airport Delay'
      }, {
        value: 'driving',
        label: 'Driving'
      }, {
        value: 'HappinessRanking',
        label: 'Happiness Ranking'
      }, {
        value: 'HollywoodsStories',
        label: 'Hollywood Stories'
      }],
      data_type: {
        'temporal': 'T',
        'quantitative': 'Q',
        'nominal': 'N',
        'ordinal': 'O'
      },
      task_list: [
        {
          task: 'Change Over Time',
          description: 'Analyse how the data changes over time series.'
        }, {
          task: 'Characterize Distribution',
          description: 'Characterize the distribution of the data over the set.'
        }, {
          task: 'Cluster',
          description: 'Find clusters of similar attribute values.'
        }, {
          task: 'Comparison',
          description: 'Give emphasis to comparison on different entities.'
        }, {
          task: 'Compute Derived Value',
          description: 'Compute aggregated or binned numeric derived value.'
        }, {
          task: 'Correlate',
          description: 'Determine useful relationships between the columns.'
        }, {
          task: 'Determine Range',
          description: 'Find the span of values within the set.'
        }, {
          task: 'Deviation',
          description: 'Compare data with certain value like zero or mean.'
        }, {
          task: 'Error Range',
          description: 'Summarizes an error range of quantitative values.'
        },
        //   {
        //     task: 'Filter',
        //     description: 'Find data cases satisfying the given constrains.'
        //   },
        {
          task: 'Find Anomalies',
          description: 'Identify any anomalies within the dataset.'
        }, {
          task: 'Find Extremum',
          description: 'Find extreme values of data column.'
        }, {
          task: 'Magnitude',
          description: 'Show relative or absolute size comparisons.'
        }, {
          task: 'Part to Whole',
          description: 'Show component elements of a single entity.'
        }, {
          task: 'Retrieve Value',
          description: 'Find values of specific columns.'
        }, {
          task: 'Sort',
          description: 'Rank data according to some ordinal metric.'
        }, {
          task: 'Spatial',
          description: 'Show spatial data like latitude and longitude.'
        }, {
          task: 'Trend',
          description: 'Use regression or loess to show the variation trend.'
        }
      ],
      dataset_value: '',
      max_number_of_charts: 10,
      max_number_of_charts_after_recommendation: 10, // 按下推荐按钮后确定的数值
      recommendation_mode_radio: '1',
      recommendation_mode: '0', // 按下推荐按钮后确定的数值
      ranking_scheme_radio: '1',
      data_list: [],
      chosen_data_items: [],
      chosen_task_items: [],
      task_checked: [false, false, false, false, false, false, false, false,
        false, false, false, false, false, false, false, false, false],
      display_by_task: true,
      recommendation_chart: {
        'Recos_dedup': {'R1': [], 'R2': [], 'R3': [], 'R4': []},
        'Recos_nodedup': {'R1': [], 'R2': [], 'R3': [], 'R4': []}
      },
      recommendation_data: [],
      has_recommendation: false,
      chart_dialog_visible: false
    }
  },
  methods: {
    choose_dataset (dataset) {
      this.dataset_value = dataset
      // TODO 向服务器发送请求获取数据，获取推荐参数
      console.log('select dataset ' + dataset)
      this.$axios.get('api/columns?dataset=' + dataset)
        .then(Response => {
          if (typeof Response.data[0].length === 'number') {
            this.data_list = Response.data[0]
          } else {
            this.data_list = Response.data
          }
          console.log(this.data_list)
        })
    },
    recommendation () {
      // TODO 将选中的数据发送到服务器，获取推荐图表
      let requestData = {}
      requestData['ColumnTypes'] = this.chosen_data_items
      requestData['task'] = this.chosen_task_items
      requestData['dataset'] = this.dataset_value
      requestData['mode'] = (this.recommendation_mode_radio === '1') ? 2 : 5
      this.recommendation_mode = this.recommendation_mode_radio
      this.max_number_of_charts_after_recommendation = this.max_number_of_charts
      this.$axios.post('api/Reco', requestData)
        .then(Response => {
          console.log(Response.data)
          this.has_recommendation = true
          this.recommendation_chart = Response.data['Recos']
          this.recommendation_data = Response.data['Data']
          this.paint_chart()
        })
    },
    paint_chart () {
      // TODO 绘制图表
      if (this.recommendation_mode_radio === '1') {
        if (this.display_by_task) {
          for (let i = 0; i < this.chosen_task_items.length; i++) {
            let task = this.chosen_task_items[i]
            if (this.recommendation_chart['Recos_nodedup'][task] === undefined) continue
            let R = {}
            switch (this.ranking_scheme_radio) {
              case '1':
                R = this.recommendation_chart['Recos_nodedup'][task]['R1']
                break
              case '2':
                R = this.recommendation_chart['Recos_nodedup'][task]['R2']
                break
              case '3':
                R = this.recommendation_chart['Recos_nodedup'][task]['R3']
                break
              case '4':
                R = this.recommendation_chart['Recos_nodedup'][task]['R4']
                break
            }
            for (let j = 0; j < R.length && j < this.max_number_of_charts; j++) {
              let props = this.set_chart_config(R[j]['props'])
              embed('#vega-chart-' + task + '-' + j, props).then(function (result) {}).catch(console.error)
            }
          }
        } else {
          let R = {}
          switch (this.ranking_scheme_radio) {
            case '1':
              R = this.recommendation_chart['Recos_dedup']['R1']
              break
            case '2':
              R = this.recommendation_chart['Recos_dedup']['R2']
              break
            case '3':
              R = this.recommendation_chart['Recos_dedup']['R3']
              break
            case '4':
              R = this.recommendation_chart['Recos_dedup']['R4']
              break
          }
          for (let j = 0; j < R.length && j < this.max_number_of_charts; j++) {
            let props = this.set_chart_config(R[j]['props'])
            embed('#vega-chart-' + j, props).then(function (result) {}).catch(console.error)
          }
        }
      } else if (this.recommendation_mode_radio === '2') {
        for (let i = 0; i < this.recommendation_chart.length && i < this.max_number_of_charts; i++) {
          let props = this.set_chart_config(this.recommendation_chart[i]['props'])
          embed('#vega-chart-' + i, props).then(function (result) {}).catch(console.error)
        }
      }
    },
    choose_data_item (item, index) {
      // TODO 选中数据种类
      let icon = document.getElementById('data-item-icon-' + index)
      let field = document.getElementById('data-item-field-' + index)
      for (let i = 0; i < this.chosen_data_items.length; i++) {
        if (this.chosen_data_items[i].field === item.field) {
          // 已选中，现在撤销选中
          this.chosen_data_items.splice(i, 1)
          icon.style['background'] = 'darkgrey'
          field.style['color'] = 'black'
          // console.log(this.chosen_data_items)
          return
        }
      }
      // 没选中，选中对象
      this.chosen_data_items.push(item)
      icon.style.background = 'dodgerblue'
      field.style['color'] = 'dodgerblue'
      // console.log(this.chosen_data_items)
    },
    choose_task_item (item, index) {
      let taskItem = document.getElementById('task-item-' + index)
      let name = document.getElementById('task-item-name-' + index)
      for (let i = 0; i < this.chosen_task_items.length; i++) {
        if (this.chosen_task_items[i] === this.transform_task_name(item.task)) {
          // 已选中，现在撤销选中
          this.chosen_task_items.splice(i, 1)
          name.style['color'] = 'black'
          taskItem.style['border-left-width'] = '0'
          console.log(this.chosen_task_items)
          return
        }
      }
      // 没选中，选中对象
      this.chosen_task_items.push(this.transform_task_name(item.task))
      name.style['color'] = 'dodgerblue'
      taskItem.style['border-left-width'] = '4px'
      console.log(this.chosen_task_items)
    },
    display_by_task_change () {
      this.paint_chart()
    },
    show_chart_dialog (task, index) {
      this.chart_dialog_visible = true
      let props = {}
      if (this.recommendation_mode_radio === '1') {
        let R = 'R1'
        switch (this.ranking_scheme_radio) {
          case '1':
            R = 'R1'
            break
          case '2':
            R = 'R2'
            break
          case '3':
            R = 'R3'
            break
          case '4':
            R = 'R4'
            break
        }
        if (this.display_by_task) {
          props = this.set_dialog_chart_config(this.recommendation_chart['Recos_nodedup'][task][R][index]['props'])
        } else {
          props = this.set_dialog_chart_config(this.recommendation_chart['Recos_dedup'][R][index]['props'])
        }
      } else {
        props = this.set_dialog_chart_config(this.recommendation_chart[index]['props'])
      }
      console.log(props)
      embed('#dialog-chart', props)
        .then(function (result) {
        }).catch(console.error)
    },
    set_chart_config (props) {
      props['data'] = {'name': 'table', 'values': this.recommendation_data}
      props['height'] = 200
      props['width'] = 200
      if (props['encoding'] === undefined) {
        props['encoding'] = {}
      }
      if (props['encoding']['x'] === undefined) {
        props['encoding']['x'] = {}
      }
      if (props['encoding']['x']['axis'] === undefined) {
        props['encoding']['x']['axis'] = {}
      }
      props['encoding']['x']['axis']['labelAngle'] = -45

      return props
    },
    set_dialog_chart_config (props) {
      props['height'] = 600
      props['width'] = 1400
      // delete props['height']
      // delete props['width']
      return props
    },
    show_more_chart (task) {
      let box = document.getElementById('vega-chart-box-by-' + task)
      let title = document.getElementById('vega-chart-box-title-' + task)
      if (box.style['height'] === 'auto') {
        title.style['width'] = 'fit-content'
        box.style['height'] = '300px'
      } else {
        title.style['width'] = '500px'
        box.style['height'] = 'auto'
      }
    },
    ranking_change () {
      this.paint_chart()
    },
    generate_id (baseId, index) {
      return baseId + index
    },
    transform_task_name (taskName) {
      return taskName.toLowerCase().replace(/ /g, '_')
    },
    transform_from_task_name (transTaskName) {
      let s = transTaskName.replace(/_/g, ' ')
      let ss = s.toLowerCase().split(/\s+/)
      for (let i = 0; i < ss.length; i++) {
        ss[i] = ss[i].slice(0, 1).toUpperCase() + ss[i].slice(1)
      }
      return ss.join(' ')
    }
  }
}
</script>

<style>
#page {
  /*display: flex;*/
  /*flex-direction: column;*/
  /*height: 1200px;*/
}

#title {
  font-size: 25px;
  color: white;
  padding: 16px;
}

#title-bar {
  background: dodgerblue;
}

#main-part {
  display: flex;
  flex-direction: row;
  /*align-items: stretch;*/
  /*height: 100%*/
}

#left-part {
  width: 340px;
  display: flex;
  flex-direction: column;
  margin-right: 5px;
}

#mid-part {
  width: 300px;
  flex-shrink: 0;
  margin-right: 5px;
  display: flex;
  flex-direction: column;
}

#right-part {
  display: flex;
  flex-direction: column;
  width: auto;
  flex-shrink: 1;
  flex-grow: 1;
}

#max-number-of-charts {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.card {
  margin-bottom: 10px;
}

.setting-title {
  margin-right: 10px;
  font-size: 13px;
}

#task-list-card {
  /*max-height: 80%;*/
  overflow-y: auto;
}

#data-box{
  max-height: 365px;
  overflow-y: auto;
}

.data-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 2px 0 3px 0;
  padding: 5px 0 5px 5px;
}

.data-item:hover {
  background-color: gainsboro;
  cursor: pointer;
}

.data-item-icon {
  border-radius: 100%;
  height: 40px;
  width: 40px;
  color: white;
  background: darkgrey;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.data-item-type {
  color: darkgray;
  font-size: small;
}

.data-item-text {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: flex-start;
}

#task-box {
  height: 908px;
  overflow-y: scroll;
}

.task-item {
  display: flex;
  flex-direction: column;
  padding: 5px 5px 5px 5px;
  border-color: dodgerblue;
  border-style: solid;
  border-width: 0;
}

.task-item:hover {
  background-color: gainsboro;
  cursor: pointer;
}

.task-item-description {
  color: darkgray;
  font-size: small;
}

#right-setting-part {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 10px 10px;
}

#display-by-task-switch {
  margin: 10px 20px 10px 0px;
}

#task_tag_box {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 5px 0 5px 0;
}

#combination-recommendation-charts {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: flex-start;
}

.task-tag {
  margin: 2px 5px 2px 0;
}

.vega-chart-box {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  flex-wrap: wrap;
  margin: 10px 20px;
}

.vega-chart-box-by-task {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  flex-wrap: wrap;
  height: 300px;
  overflow: hidden;
  margin: 10px 20px;
}

.vega-chart-box-title {
  font-size: larger;
  padding-left: 20px;
  background: dodgerblue;
  color: white;
  width: fit-content;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  cursor: pointer;
}

.vega-chart {
  margin: 20px 20px;
}

.vega-chart-task-title {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 250px;
  padding: 0 10px;
}

.vega-chart-task-title-tag {
  margin: 2px;
}

.triangle-left {
  margin-left: 20px;
  width: 0;
  height: 0;
  border-top: 20px solid transparent;
  border-right: 50px solid white;
  border-bottom: 20px solid transparent;
}

#chart-part {
  height: 890px;
  overflow-y: auto;
}

.card-logo {
  height: 30px;
  width: 30px;
  margin-right: 10px;
}

.card-title {
  display: flex;
  align-items: center;
  font-size: 20px;
}
</style>
