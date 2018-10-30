(defproject cs581-a8-twitter "0.1.0-SNAPSHOT"
  :description "cs581 assignment 8 -- twitter api"
  :url "https://github.com/khayyamsaleem/cs581"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [
                 [org.clojure/clojure   "1.8.0"]
                 [org.slf4j/slf4j-nop  "1.7.22"]
                 [yogthos/config        "1.1.1"]
                 [twitter-api           "1.8.0"]
                 [cheshire              "5.8.1"]
                 [damionjunk/nlp        "0.3.0"]
                 ]
  :main cs581-a8-twitter.core
  :aot [cs581-a8-twitter.core]
  :target-path "target/%s"
  :profiles {
             :dev {:resource-paths ["config/dev"]}
             })
