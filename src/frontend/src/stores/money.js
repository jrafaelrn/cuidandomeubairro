import Vapi from 'vuex-rest-api'
import { baseUrls } from '@/configs'
import { http } from '@/utils'

// Gastos Abertos
export default new Vapi({
  axios: http,
  baseURL: baseUrls.despesas,
  state: {
    yearPoints: {},
    years: [],
    yearInfo: null,
    pointInfo: {},
    updates: [],
    page: {},
    multiPontinfo: {}
  }
}).get({
  action: 'getYearPoints',
  property: 'yearPoints',
  path: ({ year }) => `/minlist/${year}?state=1&capcor=1`,
  onSuccess: (state, payload, axios, { params }) => {
    // Avoid state update if same data. This avoids map recreation.
    if (!state.yearPoints.features ||
        (payload.data.FeatureColletion[0].properties.uid !==
         state.yearPoints.features[0].properties.uid)
    ) {
      console.log('Payload Data: ', payload.data)
      state.yearPoints = payload.data.features
      }
      console.log('Year points retrieved from /minlist: ', state.yearPoints)
    }
}).get({
  action: 'getYears',
  property: 'years',
  path: `/info`,
  onSuccess: (state, payload, axios) => {
    state.years = payload.data.data.years.reverse()
    console.log('Years retrieved: ', state.years)
  }
}).get({
  action: 'getYearInfo',
  property: 'yearInfo',
  path: ({ year }) => `/info/${year}`,
  onSuccess: (state, payload, axios) => {
    state.yearInfo = payload.data.data
  }
}).get({
  action: 'getPointInfo',
  property: 'pointInfo',
  path: ({ code }) => `/list?code=${code}`,
  onSuccess: (state, payload, axios) => {
    state.pointInfo = payload.data.data[0]
  }
}).get({
  action: 'getMoneyPage',
  property: 'page',
  path: ({ year, page }) => `/list?year=${year}&page=${page}&per_page_num=25`,
  onSuccess: (state, payload, axios) => {
    payload.data.totalRows = payload.headers['x-total-count']
    state.page = payload.data
  }
}).get({
  action: 'getMoneyUpdates',
  property: 'updates',
  path: `/updates?per_page_num=20&has_key=state`,
  onSuccess: (state, payload, axios) => {
    // Substitute strings for Dates
    for (let row of payload.data.data) {
      row.date = new Date(row.date)
    }
    state.updates = payload.data.data
  }
}).post({
  action: 'getMultiPointInfo',
  property: 'multiPointInfo',
  path: `/list`,
  onSuccess: (state, payload, axios) => {
    let dict = {}
    for (let i of payload.data.data) {
      dict[i.code] = i
    }
    state.multiPontinfo = dict
  }
}).getStore()
