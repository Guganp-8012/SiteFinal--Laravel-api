<?php

namespace App\Http\Controllers;

use App\Models\Servico;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class ServicoController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $servicos = Servico::with('empresa','categoria')->get();

        return response()->json([
            'status' => True,
            'servicos' => $servicos
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
        $servico = Servico::create($request->all());

        return response()->json([
            'status' => true,
            'message' => "Servico criada com sucesso!",
            'servico' => $servico
        ], 200);
    }

    /**
     * Display the specified resource.
     */
    public function show($id)
    {
        $servico = Servico::with('empresa','categoria')->find($id);

        if (!$servico) {
            return response()->json(['message' => 'Servico não encontrado'], 404);
        }

        return response()->json([
            'status' => true,
            'servico' => $servico
        ]);
    }
    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Servico $servico)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, $id)
    {
        $servico = Servico::find($id);
        if (!$servico) {
            return response()->json(['message' => 'Servico não encontrado'], 404);
        }

        $validator = Validator::make($request->all(), [
            'tipo' => 'string|max:255',
            'valor' => 'numeric',
            'empresa_id' => 'integer',
            'categoria_id' => 'integer',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $servico->update($request->all());

        return response()->json([
            'status' => true,
            'message' => "Servico atualizado com sucesso!",
            'servico' => $servico
        ], 200);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy($id)
    {
        $servico = Servico::find($id);
        if (!$servico) {
            return response()->json(["message" => "Servico não encontrado"], 404);
        }

        $servico->delete();
        return response()->json(["message" => "Servico removido com sucesso"]);
    }
}