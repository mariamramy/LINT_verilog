module Edge_Cases ( data_out ) ;
 output reg data_out;
 reg A;

 always @(*)
    begin
        case (A)
        1'b0 : A = 1'b1 ;
        1'b1 : A = 1'b0 ;
        endcase
    end
 endmodule

module Vector_Input ( data_out ) ;
 output reg [1:0 ] data_out ;
 reg [ 1:0 ] A ;

 always @(*)
    begin
        case (A)
        2'b00 : A = 2'b1 ;
        2'b01 : A = 2'b0 ;
        endcase
    end
 endmodule
