<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('ordem_servicos', function (Blueprint $table) {
            $table->date('data_finalizacao')->nullable(); // Adiciona a coluna 'data_finalizacao'
            $table->boolean('status')->default(false);   // Adiciona a coluna 'status' com valor padrão false
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('ordem_servicos', function (Blueprint $table) {
            $table->dropColumn('data_finalizacao'); // Remove a coluna 'data_finalizacao'
            $table->dropColumn('status');  // Remove a coluna 'status'
        });
    }
};