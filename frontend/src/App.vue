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
               class="clearfix">
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
               class="clearfix">
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
                      label="1">Complexity-based ranking</el-radio>
            <el-radio v-model="ranking_scheme_radio"
                      label="2">Reverse-complexity-based ranking</el-radio>
            <el-radio v-model="ranking_scheme_radio"
                      label="3">Interested-data-columns-based ranking</el-radio>
            <el-radio v-model="ranking_scheme_radio"
                      label="4">Tasks-coverage-based ranking</el-radio>
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
               class="clearfix">
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
          <el-switch v-model="display_by_task" active-text="Display by task"></el-switch>
          <div id="task_tag_box">
            <el-tag class="task-tag" v-for="item in chosen_task_items" v-bind:key="item">{{transform_from_task_name(item)}}</el-tag>
          </div>
        </div>
        <el-divider></el-divider>
        <div id="chart-part">

        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
      recommendation_mode_radio: '1',
      ranking_scheme_radio: '1',
      data_list: [],
      chosen_data_items: [],
      chosen_task_items: [],
      task_checked: [false, false, false, false, false, false, false, false,
        false, false, false, false, false, false, false, false, false],
      display_by_task: false
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
      requestData['mode'] = (this.recommendation_mode_radio === 1) ? 2 : 5

      this.$axios.post('api/Reco', requestData)
        .then(Response => {
          console.log(Response.data)
        })
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
    generate_id (baseId, index) {
      return baseId + index
    },
    transform_task_name (taskName) {
      return taskName.toLowerCase().replace(/ /g, '_')
    },
    transform_from_task_name (transTaskName) {
      return transTaskName.replace(/_/g, ' ')
    }
  }
}
</script>

<style>
#page {
  /*display: flex;*/
  /*flex-direction: column;*/
  height: 1200px;
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
  max-height: 30%;
  overflow-y:auto;
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

#task_tag_box {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 5px 0 5px 0;
}

.task-tag {
  margin: 2px 5px 2px 0;
}
</style>
