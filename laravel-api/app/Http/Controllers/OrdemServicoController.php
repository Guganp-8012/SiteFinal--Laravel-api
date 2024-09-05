<?php

namespace App\Http\Controllers;

use App\Models\OrdemServico;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class OrdemServicoController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $ordem_servicos = OrdemServico::with('cliente','servico','empresa')->get();

        return response()->json([
            "status" => true,
            "ordem_servicos" => $ordem_servicos
        ]);
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $ordem_servico = OrdemServico::create($request->all());

        return response()->json([
            'status' => true,
            'message' => "Ordem de serviço criada com sucessa",
            'ordem_servico' => $ordem_servico
        ], 200);
    }

    /**
     * Display the specified resource.
     */
    public function show($id)
    {
        $ordem_servico = OrdemServico::with('cliente','servico','empresa')->find($id);

        if (!$ordem_servico) {
            return response()->json(['message' => 'Ordem de serviço não encontrada'], 404);
        }

        return response()->json([
            'status' => true,
            'ordem_servico' => $ordem_servico
        ]);
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(OrdemServico $ordem_servico)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, $id)
    {
        $ordem_servico = OrdemServico::find($id);
        if (!$ordem_servico) {
            return response()->json(['message' => 'Ordem de serviço não encontrada'], 404);
        }

        $validator = Validator::make($request->all(), [
            'cliente_id' => 'integer',
            'servico_id' => 'integer',
            'data_inicio' => 'date',
            'data_finalizacao' => 'date',
            'status' => 'boolean',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $ordem_servico->update($request->all());

        return response()->json([
            'status' => true,
            'message' => "Ordem de serviço atualizado com sucessa!",
            'ordem_servico' => $ordem_servico
        ], 200);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy($id)
    {
        $ordem_servico = OrdemServico::find($id);
        if (!$ordem_servico) {
            return response()->json(["message" => "Ordem de serviço não encontrada"], 404);
        }

        $ordem_servico->delete();
        return response()->json(["message" => "Ordem de serviço removida com sucesso"]);
    }
}
