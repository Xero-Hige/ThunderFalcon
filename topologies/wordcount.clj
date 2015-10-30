(ns wordcount
  (:use     [streamparse.specs])
  (:gen-class))

(defn wordcount [options]
   [
    ;; spout configuration
    {"word-spout" (python-spout-spec
          options
          "spouts.words.WordSpout"
          ["word"]
          )
    }
    ;; bolt configuration
    {"count-bolt" (python-bolt-spec
          options
          {"word-spout" :shuffle}
          "bolts.wordcount.WordCounter"
          ["word" "count"]
          :p 2
          )
    }
    {"count-boltz" (python-bolt-spec
          options
          {"count-bolt" :shuffle}
          "bolts.wordcount2.WorldCounter"
          ["word" "count"]
          :p 2
          )
    }

  ]
)
