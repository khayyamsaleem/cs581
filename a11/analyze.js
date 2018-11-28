const like_data = require(`./${process.argv[2]}`)
const friends_data = require(`./${process.argv[3]}`).friends.map(o => ({name: o.name, timestamp: o.timestamp*1000}))
const _ = require('underscore')
const moment = require('moment')

times_and_reacts = like_data.reactions.map(
    it => ({
        timestamp: it.timestamp*1000,
        reaction: it.data[0].reaction.reaction
    })
)

const reacts_grouped_by_month = _.groupBy(
    times_and_reacts,
    (obj) => moment(obj.timestamp).startOf('month').format()
)

let reacts_grouped_by_month_counts = {}

Object.keys(reacts_grouped_by_month).forEach(
    key => reacts_grouped_by_month_counts[(new Date(key))
        .toLocaleDateString('en-US')] = reacts_grouped_by_month[key].length
)

//console.log(reacts_grouped_by_month_counts)

const friends_data_by_month = _.groupBy(
    friends_data,
    (obj) => moment(obj.timestamp).startOf('month').format()
)
// console.log(friends_data_by_month)

let friends_data_by_month_counts = {}
Object.keys(friends_data_by_month).forEach(
    key => friends_data_by_month_counts[(new Date(key))
        .toLocaleDateString('en-US')] = friends_data_by_month[key].length
)

//console.log(friends_data_by_month_counts)

let combined = {}
Object.keys(reacts_grouped_by_month_counts).forEach(
    key => combined[key] = {
        num_friends_added : friends_data_by_month_counts[key],
        reacts : reacts_grouped_by_month_counts[key]
    }
)

console.log(JSON.stringify(combined))
