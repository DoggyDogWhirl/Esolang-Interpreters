-- Labra interpreter
-- Labra and interpreter by DoggyDogWhirl
-- the OUTPUT function "A{}" does not work in this interpreter due to Haskell's strict IO rules.

import Data.List

codeFile = "code.txt"
userInput = [1]

-- put code in a different file ("code.txt" by default)
-- user input is a list of numbers

main = do
  rawCode <- readFile codeFile
  let code = formatCode rawCode
  let results = Array [evaluate Nothing line resultInput results n | (line, n) <- zip code [0..] ]
  putStrLn "== Labra Interpreter ==\n==(cannot OUTPUT A{})=="
  putStrLn . output . last $ (unarray results)



-- Convert file to string, filter characters, check parens matching
formatCode :: String -> [Hive]
formatCode c = map (fst.bee) . checkCode . filterCode $ c
    where filterCode x = lines [ chr | chr <- x, chr `elem` "()[]{}<>\n"]
          checkCode x = if any (not.parentheses) x
                      then error "mismatched parentheses.\nI don't know where I'm just a computer"
                      else x

-- by u/repaj, checks if parens are matched
parentheses :: String -> Bool 
parentheses = null . foldr go []
  where go '(' (')' : xs) = xs
        go '[' (']' : xs) = xs
        go '{' ('}' : xs) = xs
        go '<' ('>' : xs) = xs
        go x xs = x : xs


-- Converts code into tree-like type
data Hive = Nil | Cell Char | Bee Char Hive Hive deriving (Eq, Show)

bee :: String -> (Hive, String) -- This had better work
bee [] = (Nil, "")
bee (x:xs)
  | x `elem` "([{<" = (Bee x (fst b) (fst bb), snd bb)
  | x `elem` ">}])" = (Nil, xs)
  | otherwise = error "you fricked up somehow"
  where b = bee xs
        bb = bee(snd b)


-- I guess Haskell wasn't the language for this
data Result = Scalar Int | Array [Result] deriving (Eq, Show)

unscalar (Scalar a) = a
unarray (Array a) = a
unarray (Scalar a) = error "Integer where List was necessary.\nDid you try SUMming or MAPping a single number?"

resultInput = Array . map Scalar $ userInput


--          argument        code    input     results   line#  result
evaluate :: Maybe Result -> Hive -> Result -> Result -> Int -> Result
evaluate (Just a) Nil _ _ _ = a
evaluate Nothing  Nil _ _ _ = error "Frankly, I'm not sure what you did. Sorry"

-- ()  1  SUM  +1  APPEND
evaluate Nothing  (Bee '(' Nil xs) i rs l = evaluate (Just y) xs i rs l where y = Scalar 1
evaluate Nothing  (Bee '(' x   xs) i rs l = evaluate (Just y) xs i rs l where y = foldl1 add . unarray $ (evaluate Nothing x i rs l)
evaluate (Just a) (Bee '(' Nil xs) i rs l = evaluate (Just y) xs i rs l where y = add a (Scalar 1)
evaluate (Just a) (Bee '(' x   xs) i rs l = evaluate (Just y) xs i rs l where y = add a (evaluate Nothing x i rs l)

-- []  0  INDICES  ENCLOSE  INDUCTION
evaluate Nothing  (Bee '[' Nil xs) i rs l = evaluate (Just y) xs i rs l where y = Scalar 0
evaluate Nothing  (Bee '[' x   xs) i rs l = evaluate (Just y) xs i rs l where y = indices (evaluate Nothing x i rs l)
evaluate (Just a) (Bee '[' Nil xs) i rs l = evaluate (Just y) xs i rs l where y = enclose a
evaluate (Just a) (Bee '[' x   xs) i rs l = evaluate (Just y) xs i rs l where y = induction a (\aa -> evaluate Nothing x aa rs l)

-- {}  ARG  REPEAT  OUTPUT  MAP
evaluate Nothing  (Bee '{' Nil xs) i rs l = evaluate (Just y) xs i rs l where y = i
evaluate Nothing  (Bee '{' x   xs) i rs l = evaluate (Just y) xs i rs l where y = Array . repeat $ (evaluate Nothing x i rs l)
evaluate (Just a) (Bee '{' Nil xs) i rs l = evaluate (Just y) xs i rs l where y = a
evaluate (Just a) (Bee '{' x   xs) i rs l = evaluate (Just y) xs i rs l where y = Array . map (\aa -> evaluate Nothing x aa rs l) . unarray $ a

-- <>  PREVIOUS  CALL  INVERT  INDEX
evaluate Nothing  (Bee '<' Nil xs) i rs l = evaluate (Just y) xs i rs l where y = index rs (Scalar (l-1))
evaluate Nothing  (Bee '<' x   xs) i rs l = evaluate (Just y) xs i rs l where y = index rs (evaluate Nothing x i rs l)
evaluate (Just a) (Bee '<' Nil xs) i rs l = evaluate (Just y) xs i rs l where y = invert a
evaluate (Just a) (Bee '<' x   xs) i rs l = evaluate (Just y) xs i rs l where y = index a (evaluate Nothing x i rs l)



add :: Result -> Result -> Result
add (Scalar a) (Scalar b) = Scalar (a+b)
add (Scalar a) (Array b)  = Array ((Scalar a):b)
add (Array a) (Scalar b)  = Array (a++[Scalar b])
add (Array a) (Array b)   = Array (a++b)

enclose :: Result -> Result
enclose a = Array [a]

indices :: Result -> Result
indices (Scalar a) = Array . map Scalar . take a $ [0..]
indices (Array a) = Array [Scalar i | (_, i) <- zip a [0..] ]

nest :: (a -> a) -> a -> Int -> a
nest _ s 0 = s
nest f s r = f (nest f s (r-1))

induction :: Result -> (Result -> Result) -> Result
induction s f = Array . map (nest f s) $ [0..]

index :: Result -> Result -> Result
index (Scalar l) _ = error "attempted to index from single number"
index (Array l) (Scalar i) = l !! i
index l (Array i) = Array [index l x | x <- i]

invert :: Result -> Result
invert (Scalar n) = Scalar (-n)
invert (Array l) = Array [Scalar . maybe (error "invalid index into inverted list") id . elemIndex (Scalar x) $ l | x <- [0..]]

output :: Result -> String
output (Scalar a) = show a
output (Array a) = "[" ++ (intercalate ", " . map output $ a) ++ "]"
