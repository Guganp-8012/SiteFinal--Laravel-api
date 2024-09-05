<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OrdemServico extends Model
{
    use HasFactory;
    protected $fillable = ['cliente_id','empresa_id','servico_id','data_inicio','data_finalizacao','status'];

    public function cliente()
    {
        return $this->belongsTo (cliente::class);
    }

    public function empresa()
    {
        return $this->belongsTo (empresa::class);
    }
    
    public function servico()
    {
        return $this->belongsTo (servico::class);
    }
}