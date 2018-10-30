(ns cs581-a8-twitter.core
  (:gen-class)
  (:use [twitter.oauth]
        [twitter.callbacks]
        [twitter.callbacks.handlers]
        [twitter.api.restful]
        [twitter.api.streaming])

  (:require [clojure.data.json :as json]
            [http.async.client :as ac]
            [twitter.api.search :refer [search]]
            [cheshire.core :refer :all]
            [damionjunk.nlp.stanford :refer :all]
            [config.core :refer [env]])
  (:import [twitter.callbacks.protocols AsyncStreamingCallback]))


(def my-creds (make-oauth-creds
               (:app-consumer-key env)
               (:app-consumer-secret env)
               (:user-access-token env)
               (:user-access-token-secret env)))

(defn -main [& args]
  (if-not (empty? args)
    (with-open [client (ac/create-client)]
      (doseq [arg args]
        (clojure.pprint/pprint
         (map 
          #(merge
            {:query arg}
            (first (sentiment-maps (:full_text %1)))
            {:favorite_count (:favorite_count %1)}
            {:screen_name (get-in %1 [:user :screen_name])})
                                        ;list
          (:statuses
           (:body
            (search
             :client client
             :oauth-creds my-creds
             :params {:q arg :count 20 :result_type "popular" :tweet_mode "extended"})))))))
    (throw (Exception. "Must have at least one argument!"))))
