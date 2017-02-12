HEADER = """% 1. Title: Tweet sentiment database
%
@RELATION twt

@ATTRIBUTE 1st_p_pro    NUMERIC
@ATTRIBUTE 2nd_p_pro    NUMERIC
@ATTRIBUTE 3rd_p_pro    NUMERIC
@ATTRIBUTE coord_conj   NUMERIC
@ATTRIBUTE pst_ts_vb    NUMERIC
@ATTRIBUTE ftr_ts_vb    NUMERIC
@ATTRIBUTE commas       NUMERIC
@ATTRIBUTE colons       NUMERIC
@ATTRIBUTE dashes       NUMERIC
@ATTRIBUTE parenths     NUMERIC
@ATTRIBUTE ellipse      NUMERIC
@ATTRIBUTE common_nn    NUMERIC
@ATTRIBUTE proper_nn    NUMERIC
@ATTRIBUTE adverb       NUMERIC
@ATTRIBUTE wh_words     NUMERIC
@ATTRIBUTE mdn_slang    NUMERIC
@ATTRIBUTE uppercase    NUMERIC
@ATTRIBUTE avg_sent_len NUMERIC
@ATTRIBUTE avg_tok_len  NUMERIC
@ATTRIBUTE num_sent     NUMERIC
@ATTRIBUTE class        {0, 4}

@DATA"""