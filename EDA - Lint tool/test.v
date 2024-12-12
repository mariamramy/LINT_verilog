module CaseZ_Parallel_Case (A);
 input reg [ 3:0 ] A ;
 reg [ 1:0 ] F ;

always @(*)
begin
    casez(A)
        4'b ???1: F = 2'b00 ;
        4'b ??1?: C = 2'b01 ;
        4'b ?1??: D = 2'b10 ;
        4'b 1???: E = 2'b11 ;
    endcase
end
endmodule
