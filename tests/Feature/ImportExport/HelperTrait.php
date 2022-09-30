<?php

namespace Tests\Feature\ImportExport;

use ProcessMaker\ImportExport\Exporter;
use ProcessMaker\ImportExport\Importer;
use ProcessMaker\ImportExport\Options;
use ProcessMaker\Managers\SignalManager;
use ProcessMaker\Models\Process;
use ProcessMaker\Models\ProcessCategory;
use ProcessMaker\Models\SignalData;
use SignalSeeder;

trait HelperTrait
{
    public function createProcess($bpmnPath, $attrs = [])
    {
        $bpmn = file_get_contents(__DIR__ . '/fixtures/' . $bpmnPath . '.bpmn.xml');

        return factory(Process::class)->create(
            array_merge(
                $attrs,
                [
                    'bpmn' => $bpmn,
                ]
            )
        );
    }

    public function runExportAndImport($name, $model, $between)
    {
        factory(ProcessCategory::class)->create(['is_system'=> true]);
        (new SignalSeeder())->run();
        $signal = new SignalData('test_global_signal', 'test global signal', '');
        SignalManager::addSignal($signal);

        $exporter = new Exporter();
        $exporter->$name($model);
        $payload = $exporter->payload();

        $between();

        $options = new Options([]);
        $importer = new Importer($payload, $options);
        $importer->doImport();
    }
}
